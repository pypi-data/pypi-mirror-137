import React, { useEffect, useState } from 'react';
import StyledStatusIndicator from './StatusIndicator';
import { requestAPI } from '../../handler';
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { Instance } from './types';
import { faHistory } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IInstanceList {
  className?: string;
  onlyTracked?: boolean;
}

const InstanceList = ({
  className,
  onlyTracked
}: IInstanceList): JSX.Element => {
  // ------------------------------------
  // Set up state
  // ------------------------------------
  const [instances, setInstances] = useState<Instance[]>([]);
  const [trackedInstances, setTrackedInstances] = useState<Instance[]>([]);

  // ------------------------------------
  // Handle instance initialisation
  // ------------------------------------
  const getInstances = async () => {
    const instances = await requestAPI<any>('instances');
    const instanceList: Instance[] = Object.values(instances);
    const trackedInstanceList = instanceList.filter((I: Instance) =>
      ['UNKNOWN', 'LAUNCHED'].includes(I.status)
    );

    setInstances(instanceList);
    setTrackedInstances(trackedInstanceList);
  };

  useEffect(() => {
    getInstances();
  }, []);

  // ------------------------------------
  // Handle updating instances
  // ------------------------------------
  // Note: this should be changed to a single get request
  const updateTrackedInstances = async () => {
    const tracked = await Promise.all(
      trackedInstances.map(async I => {
        return await requestAPI<any>(`instances/${I.id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        });
      })
    );
    setTrackedInstances(tracked);
  };

  useEffect(() => {
    const insMonitor = setInterval(() => updateTrackedInstances(), 5000);
    return () => {
      clearInterval(insMonitor);
    };
  }, [trackedInstances]);

  // ------------------------------------
  // Handle displaying instances
  // ------------------------------------
  const sortInstances = (a: Instance, b: Instance) => {
    if (a.created_at < b.created_at) {
      return 1;
    }
    if (a.created_at > b.created_at) {
      return -1;
    }
    return 0;
  };

  const visibleInstances = onlyTracked ? trackedInstances : instances;
  const sortedVisibleInstances = visibleInstances.sort(sortInstances);

  if (sortedVisibleInstances.length === 0) {
    return (
      <div className={`instance-list ${className}`}>
        <div className="empty">
          <div>
            <h2>
              <FontAwesomeIcon icon={faHistory} />
              No workflows instances yet... 
            </h2>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`instance-list ${className}`}>
      <ul>
        {sortedVisibleInstances.map((Instance: Instance) => (
          <li>
            <div className="instance">
              <div>
                <div className="instance-header">
                  <h2>{Instance.name}</h2>
                  <span>
                    {Instance.workflow} | Created: {Instance.created_at}
                  </span>
                </div>

                <div className="instance-bar">
                  <div className="instance-status">
                    <StyledStatusIndicator status={Instance.status} />
                    <p>{Instance.status}</p>
                  </div>

                  <Link
                    className="instance-link"
                    to={`/instances/${Instance.id}`}
                  >
                    <div>View Instance</div>
                  </Link>
                </div>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledInstanceList = styled(InstanceList)`
  max-width: 1200px;
  margin: 50px auto 0 auto;

  .empty {
    width: 100%;
    height: 250px;
    display: flex;
    text-align: center;
    align-items: center;
    justify-content: center;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }

  .empty p {
    padding-bottom: 10px;
  }

  .empty svg {
    padding-right: 15px;
    color: lightgray;
  }

  > ul {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    grid-template-rows: minmax(min-content, max-content);
    grid-column-gap: 20px;
    grid-row-gap: 20px;
    list-style: none;
  }
  .instance {
    padding: 15px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }
  h3 {
    font-size: 24px;
  }
  .instance span {
    color: #333;
  }
  .instance-header h2 {
    padding: 5px 0;
  }
  .instance-header span {
    color: #a0a0a0;
    text-transform: uppercase;
    font-size: 11px;
    line-height: 1em;
    letter-spacing: 0.05em;
  }
  .instance-header {
    display: flex;
    justify-content: space-between;
    flex-direction: column-reverse;
    padding-bottom: 15px;
  }
  .instance-bar {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .instance-status {
    display: flex;
    text-transform: uppercase;
    font-size: 11px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    align-items: center;
  }
  .instance-status p {
    padding-left: 15px;
  }
  .instance-link {
    color: #005c75;
  }
  .instance-link div {
    padding: 15px 25px;
    border: 1px solid #005c75;
    color: #005c75;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
  }
  .instance-link div:hover {
    background-color: #005c75;
    color: white;
  }
`;

export default StyledInstanceList;
