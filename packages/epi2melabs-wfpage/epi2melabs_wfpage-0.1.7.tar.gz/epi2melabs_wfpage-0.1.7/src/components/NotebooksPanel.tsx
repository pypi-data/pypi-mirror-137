import React from 'react';
import styled from 'styled-components';
import StyledNotebooksList from './notebook/NotebookList';
import { IDocumentManager } from '@jupyterlab/docmanager';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------

interface INotebooksPanel {
    className?: string;
    docTrack: IDocumentManager;
    templateDir: string;
    workDir: string;
}

const NotebooksPanel = ({
    className,
    docTrack,
    templateDir,
    workDir
}: INotebooksPanel): JSX.Element => {

const handleNotebookClone = async (
    path: string, docTrack: IDocumentManager) => {
    await docTrack.copy(path, workDir).then(e => {
        docTrack.open(path)
    })
}

const handleNotebookOpen = (
    path: string, docTrack: IDocumentManager) => {
    docTrack.open(path)
}
    
return (
  <div className={`index-panel ${className}`}>
    <div className="index-panel-intro">
      <h1>EPI2ME Labs Notebooks</h1>
      <p>
        EPI2ME Labs maintains a growing collection of notebooks on a 
        range of topics from basic quality control to genome assembly. 
        These are free and open to use by anyone. Browse the list below 
        and get started.
      </p>
    </div>

    {/* Recent */}
    <div className="index-panel-section">
      <h2>Recent notebooks</h2>
          <StyledNotebooksList
            path={workDir}
            onClick={handleNotebookOpen}
            docTrack={docTrack}
            buttonText='Open notebook'
          />
    </div>

    {/* Available */}
    <div className="index-panel-section">
      <h2>Available notebooks</h2>
        <StyledNotebooksList
            path={templateDir}
            onClick={handleNotebookClone}
            docTrack={docTrack}
            buttonText='Copy and open'
        />
    </div>
  </div>
)};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledNotebooksPanel = styled(NotebooksPanel)`
  background-color: #f6f6f6;
  padding-bottom: 100px;

  .index-panel-intro {
    padding: 75px 50px 75px 50px;
    display: flex;
    align-items: center;
    flex-direction: column;
    background-color: white;
  }

  .index-panel-intro h1 {
    padding: 25px 0;
    text-align: center;
  }

  .index-panel-intro p {
    max-width: 800px;
    text-align: center;
    font-size: 16px;
    line-height: 1.7em;
  }

  .index-panel-section {
    padding: 0 35px;
    max-width: 1200px;
    margin: 50px auto 0 auto;
  }
`;

export default StyledNotebooksPanel;
