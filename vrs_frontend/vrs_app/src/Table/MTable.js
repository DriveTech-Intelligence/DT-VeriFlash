import * as React from "react";
import { useEffect } from "react";
import axios from "axios";
import { API_FETCH_FLASH_STATS } from "../Data/Apiservice";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import "./MTable.css"

const MTable = (props) => {
  
  const fetchvsrData = async () => {
    let response = await axios.post(API_FETCH_FLASH_STATS, {
      project_id: props.project,
    });
    let vsrData = response.data;
    props.setVsrData(vsrData);
  };

  const createColumns = (vsrData) => {
    const columns = [];
    Object.keys(vsrData[0]).forEach((element) => {
      columns.push({
        field: element,
        headerName: element === "id" ? "VIN" : element.toUpperCase(),
        headerAlign: "center",
        headerClassName:"mtable",
        width:
          element === "filename"
            ? 700
            : (element === "verified") |
              (element === "passed") |
              (element === "failed")
            ? 100
            : 200,
      });
    });
    return columns;
  };

  const createRows = (vsrData) => {
    const rows = vsrData;
    return rows;
  };

  useEffect(() => {
    if (Object.keys(props.project).length !== 0) {
      fetchvsrData();
    }
  }, [props.project]);

  return props.vsrData?.length ? (
    <div style={{ height: 700, width: "100%" }}>
      <DataGrid
        rows={createRows(props.vsrData)}
        columns={createColumns(props.vsrData)}
        components={{ Toolbar: GridToolbar }}
      />
    </div>
  ) : null;
};

export default MTable;
