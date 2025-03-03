import * as React from 'react';
import PropTypes from "prop-types";


const ConcertDetail = (props) => {
  if (!props.selected)
    return (
      <div>
        <h3>Select a concert to show details</h3>
      </div>
    );
  return (
    <div>
      <h2>{props.selected.name}</h2>
      <h3>Headliner: {props.selected.headliner}</h3>
      <h3>Openers: {props.selected.openers}</h3>
      <h3>Date: {props.selected.date}</h3>
      <h3>Location: {props.selected.location}</h3>


      <div className="button-container">
      <button onClick={() => props.handleFormView(props.selected)}>Edit</button>
      <button onClick={() => props.handleRemoveConcert(props.selected.id)}>
        Delete
      </button>
      </div>
    </div>
  );
};

export default ConcertDetail;

ConcertDetail.propTypes = {
    selected:PropTypes.shape({
        
    })
}