import React, { useState, useEffect } from 'react';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { Contents } from '@jupyterlab/services';
import styled from 'styled-components';
import moment from 'moment';
import { faBookOpen } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

const IPYNB = '.ipynb'


// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
export interface ITrackedNotebook {
  name: string;
  path: string;
  last_modified: string;
  onClick?: (e: string) => void;
}

const NotebooksList = ({
    path,
    onClick,
    docTrack,
    buttonText,
    className
    }: {
      path: string,
      onClick: CallableFunction,
      docTrack: IDocumentManager,
      buttonText: string;
      className?: string;
    }): JSX.Element => {
    
    // ------------------------------------
    // Set up state
    // ------------------------------------
    const [notebooks, setNotebooks] = useState<ITrackedNotebook[]>([]);
    
    const handleUpdateSections = async () => {
        setNotebooks(await getNotebooks(path, docTrack));
    }
    
    useEffect(() => {
      handleUpdateSections()
      const slotHandleUpdateSections = (e: any) => {
      handleUpdateSections()
      }
  
      const fileSignal = docTrack.services.contents.fileChanged;
      fileSignal.connect(slotHandleUpdateSections)
      return () => {
      fileSignal.disconnect(slotHandleUpdateSections)
      }
    }, [])

    // ------------------------------------
    // Notebook doctrack utilities
    // ------------------------------------
    const getFiles = async (
      path: string,
      docTrack: IDocumentManager,
    ): Promise<Contents.IModel[]> => {
      return (await Promise.all<Contents.IModel>(
        (await docTrack.services.contents.get(path))
          .content
          .map((Item: Contents.IModel) => {
            return Item.type === 'directory'
              ? null
              : Item
          })
      )).filter(Item => !!Item)
    }

    const getNotebooks = async (
      path: string,
      docTrack: IDocumentManager,
    ): Promise<ITrackedNotebook[]> => {
      return (await getFiles(path, docTrack))
        .filter((Item: any) => Item.path.endsWith(IPYNB))
        .map((Item: any): ITrackedNotebook => ({
          name: Item.name,
          path: Item.path,
          last_modified: Item.last_modified
        }));
    }

    // ------------------------------------
    // Handle formatting notebook entries
    // ------------------------------------
    const handleExtractName = (path: string): string => {
      return path.split('/').reverse()[0]
        .split('_').join(' ').split('.ipynb').join('')
    }
  
    const handleFormatUpdated = (modified: string): string => {
      return moment(modified).format("MMMM Do YYYY, h:mm:ss a")
    }
    
    if (notebooks.length === 0) {
        return (
          <div className={`notebooks-list empty ${className}`}>
            <div className="empty">
              <FontAwesomeIcon icon={faBookOpen} />
              <h2>No notebooks to display.</h2>
            </div>
          </div>
        )
    }
  
    return (
        <div className={`notebooks-list ${className}`}>
          <ul>
              {notebooks.map(Item => (
              <li>
                
                <div className="notebook">
                  <div>
                    <div className="notebook-header">
                      <span>
                        Last modified: {handleFormatUpdated(Item.last_modified)}
                      </span>
                      <h3>{handleExtractName(Item.path)}</h3>
                    </div>
                    <div className="notebook-buttons">
                      <button onClick={() => onClick(Item.path, docTrack)}>
                        {buttonText}
                      </button>
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
const StyledNotebooksList = styled(NotebooksList)`
  max-width: 1200px;
  margin: 50px auto 0 auto;

  > ul {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    grid-template-rows: minmax(min-content, max-content);
    grid-column-gap: 20px;
    grid-row-gap: 20px;
    list-style: none;
  }

  .empty {
    width: 100%;
    height: 250px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
    background-color: #ffffff;
  }

  .empty svg {
    padding-right: 15px;
    color: lightgray;
  }

  .notebook {
    padding: 15px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }
  .notebook span {
    color: #333;
  }
  .notebook-header span {
    letter-spacing: 0.05em;
    color: #a0a0a0;
    text-transform: uppercase;
    font-size: 11px;
    line-height: 1em;
    padding-bottom: 5px;
  }
  .notebook-header {
    display: flex;
    justify-content: space-between;
    flex-direction: column;
  }
  .notebook-header h3 {
    font-size: 18px;
    padding: 10px 0 15px 0;
  }
  .notebook-buttons {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .notebook-link {
    color: #1d9655;
  }
  .notebook-buttons button {
    padding: 15px 25px;
    border: 1px solid #1d9655;
    color: #1d9655;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    background-color: transparent;
    transition: 0.2s ease-in-out all;
  }
  .notebook-buttons button:hover {
    background-color: #1d9655;
    color: white;
    cursor: pointer;
  }
`;


export default StyledNotebooksList