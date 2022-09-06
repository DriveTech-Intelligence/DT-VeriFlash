import * as React from "react";
import { useEffect, useState } from "react";
import axios from "axios";
import { API_FETCH_FLASH_STATS } from "../Data/Apiservice";
import { DataGrid } from "@mui/x-data-grid";

const MTable = () => {
  const [vsrData, setVsrData] = useState({});
  const [fetchData, setFetchData] = useState(true);
  const fetchvsrData = async () => {
    let response = await axios.post(API_FETCH_FLASH_STATS, {
      project_id: "fb05e9e0-82cd-49f1-b1d7-a72d0ef81955",
    });
    // console.log(response);
    let vsrData = response.data;
    setVsrData(vsrData);
    setFetchData(false);
  };

  const createColumns = (vsrData) => {
    const columns = [];
    Object.keys(vsrData[0]).forEach((element) => {
      columns.push({ field: element, headerName: element === "id"? "VIN": element.toUpperCase() , width: 300 });
    });
    return columns;
  };

  const createRows = (vsrData) => {
    const rows = vsrData;
    return rows;
  };

  useEffect(() => {
    if (fetchData) {
      fetchvsrData();
    }
  }, [fetchData, vsrData]);

  // console.log(vsrData);

  return vsrData?.length ? (
    <div style={{ height: 700, width: "100%" }}>
      <DataGrid rows={createRows(vsrData)} columns={createColumns(vsrData)} />
    </div>
  ) : null;
};

export default MTable;
