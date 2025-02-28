import * as React from 'react';
import ConcertList from "./ConcertList";
import ConcertDetail from "./ConcertDetail";
import ConcertForm from "./ConcertForm";
import { useState, useEffect, useMemo } from "react";
import * as concertService from "../services/concertService";


const Dashboard = ({ user }) => {
  const [concertList, setConcertList] = useState([]);
  const [selected, setSelected] = useState(null);
  const [isFormOpen, setIsFormOpen] = useState(false);

  useEffect(() => {
    const fetchConcerts = async () => {
      try {
        const concerts = await concertService.index();
        if (concerts.error) {
          throw new Error(concerts.error);
        }
        setConcertList(concerts);
      } catch (error) {
        console.log(error);
      }
    };
    fetchConcerts();
  }, []);
  

  const updateSelected = (concert) => {
    if (!isFormOpen) setSelected(concert.id);
  };
  const selectedConcert = useMemo(() => {
    return concertList.find((concert) => {
      return concert.id === selected
    })
  }, [concertList, selected])
  const handleFormView = (concert) => {
    if (!concert.headliner) setSelected(null);
    setIsFormOpen(!isFormOpen);
  };

  const handleAddConcert = async (formData) => {
    try {
      const newConcert = await concertService.create(formData);

      if (newConcert.error) {
        throw new Error(newConcert.error);
      }

      setConcertList([{...newConcert}, ...concertList]);
      setIsFormOpen(false);
    } catch (error) {
      console.log(error);
    }
  };

  const handleUpdateConcert = async (formData, concertId) => {
    try {
      const updateConcert = await concertService.updateConcert(formData, concertId);
      if (updateConcert.error) {
        throw new Error(updateConcert.error);
      }

      setConcertList((prev) => { 
        return prev.map((concert) =>
          concert.id !== updateConcert.id ? concert : {
            ...updateConcert
          } 
        );
      });
      setIsFormOpen(false);
    } catch (error) {
      console.log(error);
    }
  };

  const handleRemoveConcert = async (concertId) => {
    try {
      await concertService.deleteConcert(concertId);
      setConcertList((prev)=> prev.filter((concert) => concert.id !== concertId));
      setSelected(null);
      setIsFormOpen(false);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <main>
      <h1>Welcome, { user.username }</h1>
      <ConcertList
        concertList={concertList}
        updateSelected={updateSelected}
        handleFormView={handleFormView}
        isFormOpen={isFormOpen}
        selected={selectedConcert}
      />
      {isFormOpen ? (
        <ConcertForm
          handleAddConcert={handleAddConcert}
          selected={selectedConcert}
          handleUpdateConcert={handleUpdateConcert}
        />
      ) : (
        <ConcertDetail
          selected={selectedConcert}
          handleFormView={handleFormView}
          handleRemoveConcert={handleRemoveConcert}
        />
      )}
    </main>
  );
};

export default Dashboard;