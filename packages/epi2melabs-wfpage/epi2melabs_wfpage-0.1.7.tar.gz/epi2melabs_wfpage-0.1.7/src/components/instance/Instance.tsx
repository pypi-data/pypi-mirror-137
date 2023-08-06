import React, { useEffect, useState } from 'react';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { GenericObject } from '../../types';
import { useParams, useNavigate } from 'react-router-dom';
import StyledStatusIndicator from './StatusIndicator';
import StyledLoadingSpinner from '../LoadingSpinner';
import { requestAPI } from '../../handler';
import styled from 'styled-components';
import { Instance } from './types';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IInstanceComponent {
  className?: string;
  docTrack: IDocumentManager;
  app: JupyterFrontEnd;
}

const InstanceComponent = ({
  className,
  docTrack,
  app
}: IInstanceComponent): JSX.Element => {
  // ------------------------------------
  // Set up state
  // ------------------------------------
  const navigate = useNavigate();
  const routerParams = useParams();
  const [instanceStatus, setInstanceStatus] = useState<string>('');
  const [instanceData, setInstanceData] = useState<Instance | null>(null);
  const [instanceOutputs, setInstanceOutputs] = useState<GenericObject[]>([]);
  const [instanceParams, setInstanceParams] = useState<string[] | null>(null);
  const [instanceLogs, setInstanceLogs] = useState<string[] | null>(null);
  const [selectedLog, setSelectedLog] = useState('nextflow.stdout');

  // ------------------------------------
  // Handle instance initialisation
  // ------------------------------------
  const getRelativeInstanceDir = async (instanceData: Instance) => {
    const { curr_dir, base_dir } = await requestAPI<any>('cwd');
    const rel_base_dir = base_dir.replace(curr_dir, '').replace(/^\//, '');
    const basename = instanceData.path.split('/').reverse()[0];
    return `${rel_base_dir}/instances/${basename}`;
  };

  const getInstanceData = async () => {
    const data = await requestAPI<any>(`instances/${routerParams.id}`);
    setInstanceData(data);
    setInstanceStatus(data.status);
    return data;
  };

  useEffect(() => {
    const init = async () => {
      const data = await getInstanceData();
      getInstanceParams(data);
      getInstanceLogs(data, selectedLog);
    };
    init();
    const statusMonitor = setInterval(() => getInstanceData(), 5000);
    return () => {
      clearInterval(statusMonitor);
    };
  }, []);

  // ------------------------------------
  // Get instance params / logs / outputs
  // ------------------------------------
  const getInstanceParams = async (instanceData: Instance | null) => {
    if (instanceData) {
      const encodedPath = encodeURIComponent(
        `${instanceData.path}/params.json`
      );
      const { contents } = await requestAPI<any>(
        `file/${encodedPath}?contents=true`
      );
      if (contents !== null) {
        setInstanceParams(contents);
      }
    }
  };

  const getInstanceLogs = async (
    instanceData: Instance | null,
    selectedLog: string
  ) => {
    if (instanceData) {
      const encodedPath = encodeURIComponent(
        `${instanceData.path}/${selectedLog}`
      );
      const { contents } = await requestAPI<any>(
        `file/${encodedPath}?contents=true`
      );
      if (contents !== null) {
        setInstanceLogs(contents);
      }
    }
  };

  const getInstanceOutputs = async (instanceData: Instance | null) => {
    if (instanceData) {
      const relative = await getRelativeInstanceDir(instanceData);
      const path = `${relative}/output`;
      try {
        const files = await (
          await docTrack.services.contents.get(path)
        ).content.filter((Item: any) => Item.type !== 'directory');
        setInstanceOutputs(files);
      } catch (error) {
        console.log('Instance outputs not available yet');
      }
    }
  };

  // ------------------------------------
  // Handle opening files
  // ------------------------------------
  const handleOpenOutput = (path: string) => {
    docTrack.open(path);
  };

  const handleOpenFolder = async (instanceData: Instance) => {
    const path = await getRelativeInstanceDir(instanceData);
    app.commands.execute('filebrowser:go-to-path', { path });
  };

  // ------------------------------------
  // Handle retry workflow
  // ------------------------------------
  const handleRerunWorkflow = () => {
    if (instanceData) {
      navigate(`/workflows/${instanceData.workflow}/${instanceData.id}`);
    }
  };

  // ------------------------------------
  // Handle switching logs
  // ------------------------------------
  const handleChangingLog = (path: string) => {
    if (path !== selectedLog) {
      setInstanceLogs(null);
      setSelectedLog(path);
    }
  };

  // ------------------------------------
  // Monitor instance status
  // ------------------------------------
  useEffect(() => {
    getInstanceOutputs(instanceData);
    getInstanceLogs(instanceData, selectedLog);
    if (
      ['COMPLETED_SUCCESSFULLY', 'TERMINATED', 'ENCOUNTERED_ERROR'].includes(
        instanceStatus
      )
    ) {
      return;
    } else {
      const filesMonitor = setInterval(
        () => getInstanceOutputs(instanceData),
        10000
      );
      const logsMonitor = setInterval(
        () => getInstanceLogs(instanceData, selectedLog),
        7500
      );
      return () => {
        getInstanceLogs(instanceData, selectedLog);
        getInstanceOutputs(instanceData);
        clearInterval(filesMonitor);
        clearInterval(logsMonitor);
      };
    }
  }, [instanceStatus, selectedLog]);

  // ------------------------------------
  // Handle instance deletion
  // ------------------------------------
  const handleInstanceDelete = async (d: boolean) => {
    const outcome = await requestAPI<any>(`instances/${routerParams.id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        delete: d
      })
    });
    if (d && outcome.deleted) {
      navigate('/workflows');
    }
  };

  // ------------------------------------
  // Handle find report
  // ------------------------------------
  const getReport = (instanceData: Instance): null | GenericObject => {
    let report = null;
    if (instanceOutputs.length) {
      instanceOutputs.forEach(Item => {
        if (Item.name === `${instanceData.workflow}-report.html`) {
          report = Item;
        }
      });
    }
    return report;
  };

  // ------------------------------------
  // Render loading screen
  // ------------------------------------
  if (!instanceData) {
    return (
      <div className={`instance ${className}`}>
        <div className="loading-screen">
          <p>
            Instance data is loading... (If this screen persists, check
            connection to jupyterlab server and/or labslauncher)
          </p>
          <StyledLoadingSpinner />
        </div>
      </div>
    );
  }

  const isRunning = ['LAUNCHED'].includes(instanceStatus);
  const report = getReport(instanceData);
  return (
    <div className={`instance ${className}`}>
      <div className="instance-container">
        {/* Instance header */}
        <div className="instance-section instance-header">
          <div className="instance-header-top">
            <h2 className="instance-workflow">
              Workflow: {instanceData.workflow}
            </h2>
            {isRunning ? (
              <button onClick={() => handleInstanceDelete(false)}>
                Stop Instance
              </button>
            ) : (
              ''
            )}
          </div>
          <h1>{instanceData.name}</h1>
          <div className="instance-details">
            <div className="instance-status">
              <StyledStatusIndicator status={instanceStatus || 'UNKNOWN'} />
              <p>{instanceStatus}</p>
            </div>
            <p>Created: {instanceData.created_at}</p>
            <p>Updated: {instanceData.updated_at}</p>
            <p>ID: {routerParams.id}</p>
          </div>
        </div>

        {/* Instance params */}
        <div className="instance-section instance-params">
          <div className="instance-section-header">
            <h2>Instance params</h2>
            <div className="instance-section-header-controls">
              <button onClick={() => handleRerunWorkflow()}>
                Configure and rerun
              </button>
            </div>
          </div>
          <div className="instance-section-contents">
            {instanceParams && instanceParams.length ? (
              <ul>
                {instanceParams.map(Item => (
                  <li>
                    <span>{Item}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <div>
                <StyledLoadingSpinner />
              </div>
            )}
          </div>
        </div>

        {/* Instance logs */}
        <div className="instance-section instance-logs">
          <div className="instance-section-header">
            <h2>Instance logs</h2>
            <div className="instance-section-header-controls">
              <button onClick={() => handleChangingLog('nextflow.stdout')}>
                Nextflow
              </button>
              <button onClick={() => handleChangingLog('invoke.stdout')}>
                Invoke
              </button>
            </div>
          </div>
          <div className="instance-section-contents">
            {instanceLogs && instanceLogs.length ? (
              <ul>
                {instanceLogs.map(Item => (
                  <li>
                    <span>{Item}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <div>
                <StyledLoadingSpinner />
              </div>
            )}
          </div>
        </div>

        {/* Instance outputs */}
        <div className="instance-section instance-outputs">
          <div className="instance-section-header">
            <h2>Output files</h2>
            <div className="instance-section-header-controls">
              {report ? (
                <button onClick={() => handleOpenOutput(report.path)}>
                  Open report
                </button>
              ) : (
                ''
              )}
              <button
                onClick={() =>
                  instanceData ? handleOpenFolder(instanceData) : ''
                }
              >
                Open folder
              </button>
            </div>
          </div>
          <div className="instance-section-contents">
            {instanceOutputs.length ? (
              <ul>
                {instanceOutputs.map(Item => (
                  <li>
                    <button onClick={() => handleOpenOutput(Item.path)}>
                      {Item.name}
                    </button>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="instance-section-contents">No outputs yet...</div>
            )}
          </div>
        </div>

        {/* Instance delete */}
        <div className="instance-section instance-delete">
          <div className="instance-section-header">
            <h2>Danger zone</h2>
          </div>
          <div className="instance-section-contents">
            <div className={`${!isRunning ? 'active' : 'inactive'}`}>
              <button
                onClick={() => (!isRunning ? handleInstanceDelete(true) : null)}
              >
                Delete Instance
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledInstanceComponent = styled(InstanceComponent)`
  background-color: #f6f6f6;

  .loading-screen {
    display: flex;
    justify-content: center;
    min-height: calc(100vh - 100px);
    align-items: center;
    flex-direction: column;
  }

  .loading-screen p {
    text-align: center;
    max-width: 600px;
    padding-bottom: 15px;
  }

  .instance-container {
    padding: 50px 0 100px 0 !important;
  }

  .instance-section {
    width: 100%;
    padding: 15px;
    max-width: 1200px;
    margin: 0 auto 25px auto;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
    background-color: #ffffff;
  }

  .instance-section-header {
    padding-bottom: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .instance-section-header-controls button {
    cursor: pointer;
    padding: 10px 15px;
    margin-left: 10px;
    border: none;
    color: rgba(0, 0, 0, 0.3);
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    outline: none;
    background-color: rgb(239, 239, 239);
  }

  .instance-section-header-controls button:hover {
    color: #005c75;
  }

  .instance-section-contents {
    padding: 15px;
    border-radius: 4px;
  }

  .instance-header-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
  }

  .instance-header-top button {
    cursor: pointer;
    padding: 8px 15px;
    border: 1px solid #e34040;
    color: #e34040;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    outline: none;
    background-color: transparent;
  }

  .instance-header-top button:hover {
    cursor: pointer;
    background-color: #e34040;
    color: white;
  }

  .instance-details {
    display: flex;
    align-items: center;
  }

  .instance-details p {
    padding-left: 15px;
    text-transform: uppercase;
    font-size: 11px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    color: rgba(0, 0, 0, 0.5);
  }

  .instance-status {
    display: flex;
    align-items: center;
  }

  .instance-status p {
    color: black;
    padding-left: 15px;
  }

  .instance-outputs .instance-section-contents,
  .instance-params .instance-section-contents,
  .instance-logs .instance-section-contents {
    background-color: #f6f6f6;
    font-size: 12px;
    font-family: monospace;
    overflow: auto;
    text-overflow: initial;
    max-height: 500px;
    white-space: pre;
    color: black;
    border-radius: 4px;
  }

  .instance-outputs .instance-section-contents button,
  .instance-params .instance-section-contents span,
  .instance-logs .instance-section-contents span {
    font-size: 12px;
    font-family: monospace;
  }

  .instance-outputs li {
    margin: 0 0 5px 0;
    display: flex;
    background-color: #f6f6f6;
  }

  .instance-outputs .instance-section-contents button {
    width: 100%;
    text-align: left;
    padding: 5px 0 10px 0;
    font-size: 12px;
    font-family: monospace;
    border: none;
    outline: none;
    background: transparent;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    cursor: pointer;
  }

  .instance-outputs .instance-section-contents > ul > li:last-child button {
    border-bottom: none;
    padding-bottom: 0;
  }

  .instance-outputs .instance-section-contents button:hover {
    color: #005c75;
  }

  .instance-delete .instance-section-contents {
    background-color: #f6f6f6;
  }

  .instance-delete button {
    padding: 15px 25px;
    margin: 0 15px 0 0;
    border: 1px solid lightgray;
    color: lightgray;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    outline: none;
    background-color: transparent;
  }
  .instance-delete .active button {
    border: 1px solid #e34040;
    color: #e34040;
  }
  .instance-delete .active button:hover {
    cursor: pointer;
    background-color: #e34040;
    color: white;
  }
`;

export default StyledInstanceComponent;
