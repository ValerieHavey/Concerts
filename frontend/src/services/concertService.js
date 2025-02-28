const BASE_URL = `/concerts`;

const index = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await fetch(BASE_URL, {
        headers:{
            Authorization: `Bearer ${token}`,
        }
    });
    return res.json();
  } catch (err) {
    console.log(err);
  }
};
    
const create = async (formData) => {
  try {
    const token = localStorage.getItem("token");
    const res = await fetch(BASE_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(formData),
    });
    return res.json();
  } catch (err) {
    console.log(err);
  }
};
    
const updateConcert = async (formData, concertId) => {
  try {
    const token = localStorage.getItem("token");
    const res = await fetch(`${BASE_URL}/${concertId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(formData),
    });
    return res.json();
  } catch (err) {
    console.log(err);
  }
};
    
const deleteConcert = async (concertId) => {
  try {
    const token = localStorage.getItem("token");
    await fetch(`${BASE_URL}/${concertId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  } catch (err) {
    console.log(err);
  }
};

    
    export { index, create, updateConcert, deleteConcert };