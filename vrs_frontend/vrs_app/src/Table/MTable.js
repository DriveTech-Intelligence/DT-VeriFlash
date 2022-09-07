import * as React from "react";
import { useEffect, useState } from "react";
import axios from "axios";
import { API_FETCH_FLASH_STATS } from "../Data/Apiservice";
import { DataGrid } from "@mui/x-data-grid";

const MTable = (props) => {
  const [vsrData, setVsrData] = useState({});
  const fetchvsrData = async () => {
    let response = await axios.post(API_FETCH_FLASH_STATS, {
      project_id: props.project,
    });
    let vsrData = response.data;
    setVsrData(vsrData);
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
      fetchvsrData();
  }, [props.project]);


  return vsrData?.length ? (
    <div style={{ height: 700, width: "100%" }}>
      <DataGrid rows={createRows(vsrData)} columns={createColumns(vsrData)} />
    </div>
  ) : null;
};

export default MTable;
