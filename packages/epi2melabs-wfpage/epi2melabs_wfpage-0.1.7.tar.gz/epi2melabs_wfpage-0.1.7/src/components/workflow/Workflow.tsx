import React, { useEffect, useState } from 'react';
import { requestAPI } from '../../handler';
import { useParams, useNavigate } from 'react-router-dom';
import { GenericStringObject, GenericObject } from '../../types';
import { validateSchema, parseValidationErrors } from '../../schema';
import StyledWorkflowParameterSection from './WorkflowParameterSection';
import styled from 'styled-components';
import {
  Workflow,
  WorkflowDefaults,
  ParameterSection,
  Parameter
} from './schema';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IWorkflowComponent {
  className?: string;
}

const WorkflowComponent = ({ className }: IWorkflowComponent): JSX.Element => {
  // ------------------------------------
  // Set up state
  // ------------------------------------
  const params = useParams();
  const navigate = useNavigate();
  const [workflowData, setWorkflowData] = useState<Workflow | undefined>();
  const [workflowParams, setWorkflowParams] = useState<WorkflowDefaults>({});
  const [workflowParamsValid, setWorkflowParamsValid] = useState(false);
  const [workflowParamsErrors, setWorkflowParamsErrors] =
    useState<GenericObject>({});
  const [workflowActiveSections, setWorkflowActiveSections] = useState<
    ParameterSection[]
  >([]);
  const [instanceCreateError, setInstanceCreateError] = useState<string | null>(null)
  const [instanceName, setInstanceName] = useState<string | null>();

  // ------------------------------------
  // Handle component initialisation
  // ------------------------------------
  const getWorkflowData = async () => {
    return await requestAPI<any>(`workflows/${params.name}`);
  };

  const getInstanceParams = async (instance_id: string | undefined) => {
    if (instance_id) {
      const { path } = await requestAPI<any>(`instances/${instance_id}`);
      const encodedPath = encodeURIComponent(`${path}/params.json`);
      const { exists, contents } = await requestAPI<any>(
        `file/${encodedPath}?contents=true`
      );
      if (!exists) {
        return null;
      }
      return JSON.parse(contents.join(''));
    }
  };

  const filterHiddenParameters = (parameters: { [key: string]: Parameter }) =>
    Object.entries(parameters)
      .filter(([key, Property]) => !Property.hidden && key !== 'out_dir')
      .reduce(
        (obj, prop) => ({
          [prop[0]]: prop[1],
          ...obj
        }),
        {}
      );

  const getSchemaSections = (definitions: ParameterSection[]) => {
    return definitions
      .map(Section => ({
        ...Section,
        properties: filterHiddenParameters(Section.properties)
      }))
      .filter(Def => Object.keys(Def.properties).length !== 0);
  };

  const overrideDefaults = (
    sections: ParameterSection[],
    defaults: GenericObject
  ) => {
    return sections.map(Section => ({
      ...Section,
      properties: Object.entries(Section.properties).reduce(
        (obj, prop) => ({
          [prop[0]]: {
            ...prop[1],
            default: defaults[prop[0]] || prop[1].default
          },
          ...obj
        }),
        {}
      )
    }));
  };

  useEffect(() => {
    const init = async () => {
      // Get the initial workflow data
      const workflowData = await getWorkflowData();
      setWorkflowData(workflowData);
      // Acquire the workflow default params
      const defaults = await getInstanceParams(params.instance_id);
      if (defaults) {
        setWorkflowParams(defaults);
      } else {
        setWorkflowParams(workflowData.defaults);
      }
      // Get and set the workflow schema sections
      const sections = getSchemaSections(
        Object.values(workflowData.schema.definitions)
      );
      if (defaults) {
        const overriden = overrideDefaults(sections, defaults);
        setWorkflowActiveSections(overriden);
        return;
      }
      setWorkflowActiveSections(sections);
    };
    init();
  }, []);

  // ------------------------------------
  // Handle parameter validation
  // ------------------------------------
  const filterErrorsByParameters = (
    parameters: { [key: string]: Parameter },
    errors: GenericStringObject
  ) =>
    Object.keys(parameters).reduce(
      (obj, key) =>
        Object.prototype.hasOwnProperty.call(errors, key)
          ? {
              ...obj,
              [key]: errors[key]
            }
          : obj,
      {}
    );

  const handleInputChange = (id: string, format: string, value: any) => {
    if (value === '') {
      const { [id]: _, ...rest } = workflowParams;
      setWorkflowParams(rest);
      return;
    }
    setWorkflowParams({ ...workflowParams, [id]: value });
  };

  useEffect(() => {
    if (workflowData) {
      const { valid, errors } = validateSchema(
        workflowParams,
        workflowData.schema
      );
      valid
        ? setWorkflowParamsErrors({})
        : setWorkflowParamsErrors(parseValidationErrors(errors));
      setWorkflowParamsValid(valid);
    }
  }, [workflowParams]);

  // ------------------------------------
  // Handle instance naming
  // ------------------------------------
  const handleInstanceRename = (name: string) => {
    if (name === '' || name.length > 50 || name.length < 10) {
      setInstanceName(null)
      return
    }
    setInstanceName(name)
  }

  // ------------------------------------
  // Handle workflow launch
  // ------------------------------------
  const launchWorkflow = async () => {
    if (!workflowParamsValid || !instanceName) {
      return;
    }
    const { created, instance, error } = await requestAPI<any>('instances', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        workflow: params.name,
        params: workflowParams,
        ...instanceName ? { name: instanceName } : {}
      })
    });
    if (error) {
      setInstanceCreateError(error)
    }
    if (!created) {
      return
    }
    navigate(`/instances/${instance.id}`);
  };

  return workflowData ? (
    <div className={`workflow ${className}`}>
      <div className="workflow-container">
        {/* Workflow header */}
        <div className="workflow-section workflow-header">
          <h1>Workflow: {params.name}</h1>
          <div className="workflow-description">
            <div>{workflowData.desc}</div>
          </div>
          <div className="workflow-details">
            <div>Version {workflowData.defaults.wfversion}</div>
          </div>
        </div>

        {/* Instance name */}
        <div className="workflow-section workflow-name">
          <h2>1. Name workflow run</h2>
          <div className="workflow-section-contents">
            <input
              id="worflow-name-input"
              type="text"
              placeholder={'E.g. my_experiment (Between 10 and 50 characters).'}
              onChange={e => handleInstanceRename(e.target.value)}
              maxLength={50}
            />
          </div>
        </div>

        {/* Workflow params */}
        <div className="workflow-section workflow-parameter-sections">
          <h2>2. Choose parameters</h2>
          <div className="workflow-section-contents">
            <ul>
              {workflowActiveSections.map(Section => (
                <li>
                  <StyledWorkflowParameterSection
                    title={Section.title}
                    description={Section.description}
                    fa_icon={Section.fa_icon}
                    properties={Section.properties}
                    errors={filterErrorsByParameters(
                      Section.properties,
                      workflowParamsErrors
                    )}
                    onChange={handleInputChange}
                  />
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Workflow launch */}
        <div className="workflow-section workflow-launch-control">
          <h2>3. Launch workflow</h2>
          <div className="workflow-section-contents">
            <div
              className={`launch-control ${
                workflowParamsValid && instanceName ? 'active' : 'inactive'
              }`}
            >
              <button onClick={() => launchWorkflow()}>Run command</button>
              {instanceCreateError ? (
                <div className='error'>
                    <p>Error: {instanceCreateError}</p>
                </div>
              ) : ('')}
            </div>
          </div>
        </div>
      </div>
    </div>
  ) : (
    <React.Fragment />
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledWorkflowComponent = styled(WorkflowComponent)`
  background-color: #f6f6f6;

  .workflow-container {
    padding: 0 0 100px 0 !important;
  }

  .workflow-section {
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

  .workflow-section > h2 {
    padding-bottom: 15px;
  }

  .workflow-header {
    width: 100%;
    margin: 0 auto 50px auto;
    max-width: 100%;
    box-shadow: none;
    padding: 75px 0;
    text-align: center;
  }

  .workflow-description div {
    letter-spacing: 0em;
    font-size: 14px;
    text-transform: none;
    padding-bottom: 15px;
    max-width: 700px;
    line-height: 1.4em;
    text-align: center;
    margin: 0 auto;
    color: #a0a0a0;
  }

  .workflow-details div {
    /* color: #333;
    font-weight: normal;
    font-size: 14px; */
    padding-bottom: 5px;
    color: #a0a0a0;
    text-transform: uppercase;
    font-size: 11px;
    line-height: 1em;
    letter-spacing: 0.05em;
  }

  .workflow-parameter-sections .workflow-section-contents > ul > li {
    background-color: #fafafa;
    padding: 15px;
    margin: 0 0 15px 0;
    border-radius: 4px;
  }

  .workflow-name .workflow-section-contents {
    border-radius: 4px;
    background-color: #f6f6f6;
  }

  .workflow-name input {
    margin: 0;
    box-sizing: border-box;
    width: 100%;
    padding: 15px 25px;

    font-size: 12px;
    font-family: monospace;
    letter-spacing: 0.05em;
    line-height: 1em;

    color: black;
    background-color: #f3f3f3;
    border: 0;
    border: 1px solid transparent;
    border-radius: 4px;
    outline: none;

    transition: 0.2s ease-in-out all;
  }

  .workflow-name input:hover {
    border: 1px solid #005c75;
  }

  .workflow-launch-control .workflow-section-contents {
    padding: 15px;
    border-radius: 4px;
    background-color: #f6f6f6;
  }

  .workflow-launch-control button {
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

  .workflow-launch-control .active button {
    border: 1px solid #1d9655;
    color: #1d9655;
  }
  .workflow-launch-control .active button:hover {
    cursor: pointer;
    background-color: #1d9655;
    color: white;
  }
  .workflow-launch-control .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`;

export default StyledWorkflowComponent;
