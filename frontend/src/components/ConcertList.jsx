import * as React from 'react';

const ConcertList = (props) => {
    const concerts = props.concertList.map((concert) => (
      <a key={concert.id} onClick={() => props.updateSelected(concert)}>
      {concert.id==props.selected?.id ? <li><strong>{concert.headliner}</strong></li> : <li>{concert.headliner}</li>}
      </a>
    ));
  
    return (
      <div>
          <h1> Concerts You've Attended! </h1>
          {!props.concertList.length ? <h2>No Concerts Yet!</h2> : <ul>{concerts}</ul>}
          <button onClick={props.handleFormView}>
      {props.isFormOpen ? 'Close Form' : 'New Concert'}
    </button>
      </div>
    );
  };
  
  export default ConcertList;
  