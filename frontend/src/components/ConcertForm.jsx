import * as React from 'react';
import { useState } from "react";

const ConcertForm = (props) => {
  const initialState = {
    headliner: "",
    openers: "",
    date: "",
    location: "",
    notes: ""
  }
  const [formData, setFormData] = useState(props.selected ? props.selected : initialState)

  const handleChange = (evt) => {
    setFormData({ ...formData, [evt.target.name]: evt.target.value });
  };

  const handleSubmitForm = (evt) => {
    evt.preventDefault();
    if (props.selected) {
      props.handleUpdateConcert(formData, props.selected.id);
    } else {
      props.handleAddConcert(formData);
    }
  };
 

  return (
    <div>
      <form onSubmit={handleSubmitForm}>
        <label htmlFor="headliner"> Headliner </label>
        <input
          id="headliner"
          name="headliner"
          value={formData.headliner}
          onChange={handleChange}
          required
        />
        <label htmlFor="openers"> Openers </label>
        <input
          id="openers"
          name="openers"
          value={formData.openers}
          onChange={handleChange}
          required
        />
        <label htmlFor="date"> Date of Concert </label>
        <input
          id="date"
          name="date"
          value={formData.date}
          onChange={handleChange}
          required
        />
        <label htmlFor="location"> Location of Concert </label>
        <input
          id="location"
          name="location"
          value={formData.location}
          onChange={handleChange}
          required
        />
        <label htmlFor="notes"> Notes </label>
        <textarea
          type="text"
          id="notes"
          name="notes"
          value={formData.notes ?? ""}
          onChange={handleChange}
        />
        <button type="sumbit"> {props.selected ? 'Update Concert' : 'Add New Concert'} </button>
      </form>
    </div>
  );
};

export default ConcertForm;
