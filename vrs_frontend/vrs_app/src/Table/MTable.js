import * as React from "react";
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
} from "@mui/material";
import { useEffect, useState } from "react";
// import axios from "axios";
import { API_FETCH_VSR_DATA } from "../Data/Apiservice";
import { DataGrid } from "@mui/x-data-grid";

const columns = [
  { field: "id", headerName: "ID", width: 90 },
  {
    field: "firstName",
    headerName: "First name",
    width: 150,
    // editable: true,
  },
  {
    field: "lastName",
    headerName: "Last name",
    width: 150,
    // editable: true,
  },
  {
    field: "age",
    headerName: "Age",
    // type: "number",
    width: 110,
    // editable: true,
  },
  {
    field: "fullName",
    headerName: "Full name",
    // description: "This column has a value getter and is not sortable.",
    // sortable: false,
    width: 160,
  },
];

const rows = [
  { id: 1, lastName: "Snow", firstName: "Jon", age: 35 },
  { id: 2, lastName: "Lannister", firstName: "Cersei", age: 42 },
  { id: 3, lastName: "Lannister", firstName: "Jaime", age: 45 },
  { id: 4, lastName: "Stark", firstName: "Arya", age: 16 },
  // { id: 5, lastName: "Targaryen", firstName: "Daenerys", age: null },
  // { id: 6, lastName: "Melisandre", firstName: null, age: 150 },
  // { id: 7, lastName: "Clifford", firstName: "Ferrara", age: 44 },
  // { id: 8, lastName: "Frances", firstName: "Rossini", age: 36 },
  // { id: 9, lastName: "Roxie", firstName: "Harvey", age: 65 },
];

const MTable = () => {
  const [vsrData, setVsrData] = useState({});
  const [fetchData, setFetchData] = useState(true);
  // const fetchvsrData = async () => {
  //   let response = await axios.get(API_FETCH_VSR_DATA);
  //   let vsrData = response.data;
  //   setVsrData(vsrData);
  //   setFetchData(false);
  // };

  // useEffect(() => {
  //   if (fetchData) {
  //     fetchvsrData();
  //   }
  // }, [fetchData, vsrData]);

  return (
    <div style={{ height: 700, width: "100%" }}>
      <DataGrid rows={rows} columns={columns} pageSize={12} />
    </div>
  );

  // return vsrData?.length ? (

  // ) : <TableContainer component={Paper}>
  //   <Table sx={{ minWidth: 650 }} aria-label="simple table">
  //     <TableHead>
  //       <TableRow>
  //         {vsrData &&
  //           Object.keys(vsrData[0]).map((key) => (
  //             <TableCell variant="head">{key}</TableCell>
  //           ))}
  //       </TableRow>
  //     </TableHead>
  //     <TableBody>
  //       {vsrData &&
  //         vsrData.map(
  //           (object_data, index) => (
  //             <TableRow
  //               key={index}
  //               sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
  //             >
  //               <TableCell
  //                 key={object_data.VIN}
  //                 sortDirection="asc"
  //               >
  //                 {object_data.VIN}
  //               </TableCell>
  //               <TableCell
  //                 key={object_data.Pre_flash}
  //                 // sortDirection={
  //                 //   orderBy === object_data.Pre_flash ? order : false
  //                 // }
  //               >
  //                 {object_data.Pre_flash}
  //               </TableCell>
  //               <TableCell
  //                 key={object_data.Post_flash}
  //                 // sortDirection={
  //                 //   orderBy === object_data.Post_flash ? order : false
  //                 // }
  //               >
  //                 {object_data.Post_flash}
  //               </TableCell>
  //               <TableCell
  //                 key={object_data.PWT}
  //                 // sortDirection={orderBy === object_data.PWT ? order : false}
  //               >
  //                 {object_data.PWT}
  //               </TableCell>
  //               <TableCell
  //                 key={object_data.Status}
  //                 // sortDirection={
  //                 //   orderBy === object_data.Status ? order : false
  //                 // }
  //               >
  //                 {object_data.Status}
  //               </TableCell>
  //               <TableCell
  //                 key={object_data.Date}
  //                 // sortDirection={orderBy === object_data.Date ? order : false}
  //               >
  //                 {object_data.Date}
  //               </TableCell>
  //               <TableCell
  //                 key={object_data.Filename}
  //                 // sortDirection={
  //                 //   orderBy === object_data.Filename ? order : false
  //                 // }
  //               >
  //                 {object_data.Filename}
  //               </TableCell>
  //               {/* {Object.keys(object_data).forEach((key) => {
  //                 console.log(object_data[key])
  //               })}
  //               {console.log("one here console log")} */}
  //             </TableRow>
  //           )
  //           // <TableCell>
  //           //   {Object.keys(vsrData[key]).map((colD, index) => (
  //           //     <TableRow
  //           //       key={vsrData[key][colD] + index}
  //           //       sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
  //           //     >
  //           //       <TableCell>{vsrData[key][colD]}</TableCell>
  //           //     </TableRow>
  //           //   ))}
  //           // </TableCell>
  //         )}
  //     </TableBody>
  //   </Table>
  // </TableContainer>
  // null;
};

export default MTable;
