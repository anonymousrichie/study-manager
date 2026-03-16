import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getTimetable } from "../services/api.js";

const TimetablePage = () => {
  const [data, setData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getTimetable();
        setData(result);
      } catch (error) {
        if (error.message.includes("401") || error.message.includes("Invalid")) {
          navigate("/login"); // Redirect to login
        } else {
          console.error(error);
        }
      }
    };
    fetchData();
  }, [navigate]);

  return <div>{data ? JSON.stringify(data) : "Loading..."}</div>;
};

export default TimetablePage;
