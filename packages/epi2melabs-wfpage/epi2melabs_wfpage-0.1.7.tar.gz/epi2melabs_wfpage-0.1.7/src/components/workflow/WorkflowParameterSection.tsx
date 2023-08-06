import React, { useState } from 'react';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { fab } from '@fortawesome/free-brands-svg-icons';
import { fas, faCaretDown, faCaretUp, faCheckCircle, faTimesCircle } from '@fortawesome/free-solid-svg-icons';
import { IconName, IconPrefix } from '@fortawesome/fontawesome-svg-core';
import StyledParameterComponent from './WorkflowParameter';
import { ParameterSection } from './schema';
import styled from 'styled-components';

// -----------------------------------------------------------------------------
// Component
// -----------------------------------------------------------------------------
interface IParameterSectionComponent extends ParameterSection {
  errors: { [key: string]: string[] };
  onChange: CallableFunction;
  className?: string;
}

const ParameterSectionComponent = ({
  title,
  fa_icon,
  properties,
  errors,
  onChange,
  className
}: IParameterSectionComponent): JSX.Element => {
  // ------------------------------------
  // Set up state
  // ------------------------------------
  const [isOpen, setIsOpen] = useState(false);
  const isValid = Object.keys(errors).length === 0 ? true : false;

  // ------------------------------------
  // Handle fa_icon
  // ------------------------------------
  library.add(fas, fab);
  const iconName = fa_icon?.split(' ')[1];
  const iconPrefix = fa_icon?.split(' ')[0];
  const iconNameStripped = iconName?.startsWith('fa-')
    ? iconName.split('fa-')[1]
    : iconName;

  return (
    <div className={`parameter-section ${className}`}>
      <div className={`parameter-section-container ${isValid ? 'valid' : ''}`}>
        <button
          className="parameter-section-toggle"
          onClick={() => setIsOpen(!isOpen)}
        >
          <h3>
            {typeof fa_icon === 'string' ? (
              <FontAwesomeIcon
                icon={[iconPrefix as IconPrefix, iconNameStripped as IconName]}
              />
            ) : (
              ''
            )}
            {title}
          </h3>
          <div className='parameter-section-toggle-controls'>
              {isValid ? (
                <div className='parameter-section-toggle-errors valid'>
                  <FontAwesomeIcon icon={faCheckCircle} />
                </div>
              ) : (
                <div className='parameter-section-toggle-errors invalid'>
                  <p>{Object.keys(errors).length}</p>
                  <FontAwesomeIcon icon={faTimesCircle} />
                </div>
              )}
            <FontAwesomeIcon icon={isOpen ? faCaretUp : faCaretDown} />
          </div>
        </button>
        <ul className={`parameter-section-items ${isOpen ? 'open' : 'closed'}`}>
          {Object.entries(properties).map(([key, value]) => (
            <li className="parameter">
              <StyledParameterComponent
                id={key}
                schema={value}
                error={errors[key] || []}
                onChange={onChange}
              />
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

// -----------------------------------------------------------------------------
// Component Styles
// -----------------------------------------------------------------------------
const StyledParameterSectionComponent = styled(ParameterSectionComponent)`
  .parameter-section-toggle {
    box-sizing: border-box;
    width: 100%;
    display: flex;
    padding: 15px;
    justify-content: space-between;
    align-items: center;
    border: none;
    outline: none;
    background: transparent;
    cursor: pointer;
  }

  .parameter-section-toggle h3 svg {
    margin-right: 15px;
  }

  .parameter-section-toggle h3 {
    font-size: 16px;
    font-weight: normal;
    color: #e34040;
  }

  .parameter-section-container.valid .parameter-section-toggle h3 {
    color: black;
  }

  .parameter-section-toggle-controls {
    display: flex;
  }

  .parameter-section-toggle-errors {
    margin-right: 15px;
    display: flex;
    align-items: center;
  }

  .parameter-section-toggle-errors svg {
    width: 15px;
    height: 15px;
    margin-left: 5px;
  }

  .parameter-section-toggle-errors.valid svg {
    color: #1d9655;
  }

  .parameter-section-toggle-errors.invalid svg {
    color: #e34040;
  }

  .parameter-section-toggle-errors.invalid p {
    font-weight: bold;
    color: #e34040;
  }

  .parameter-section-items {
    display: block;
    padding: 15px 15px 0 15px;
    transition: 0.2s ease-in-out all;
  }

  .parameter-section-items.closed {
    display: none;
  }

  .parameter-section-items.open {
    padding-top: 15px;
    display: block;
  }
`;

export default StyledParameterSectionComponent;
