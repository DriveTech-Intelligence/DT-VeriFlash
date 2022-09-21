import React, { useState } from "react";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { Navigate } from "react-router-dom";
import AuthContext from "../../Context/AuthProvider";
import {
  API_GET_COMPANY_BY_USERNAME,
  API_SIGN_IN,
} from "../../Data/Apiservice";
import axios from "axios";
import { useContext } from "react";

const theme = createTheme();

const Login = () => {
  const { auth, setAuth } = useContext(AuthContext);
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    if (data.get("username") !== "" || data.get("username") !== "") {
      const username = data.get("username");
      const password = data.get("password");
      var company = null;

      try {
        const response = await axios.post(API_SIGN_IN, data, {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        });

        if (response.status === 200) {
          const resp = await axios.post(
            API_GET_COMPANY_BY_USERNAME,
            {
              user: username,
            },
            {
              headers: {
                user_token: response?.data?.access_token,
              },
            }
          );
          company = resp?.data?.company;

          const accessToken = resp?.data?.token;

          setAuth({
            username,
            password,
            accessToken,
            company,
          });
        }
      } catch (err) {
        setError(err.response.data.detail);
      }
    }
  };

  return auth?.accessToken ? (
    <Navigate to="flash-stats" replace />
  ) : (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          {error !== null && (
            <Typography component="h1" variant="h5" style={{ color: "red" }}>
              {error}
            </Typography>
          )}
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <Box
            component="form"
            onSubmit={handleSubmit}
            noValidate
            sx={{ mt: 1 }}
          >
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
            <Grid container>
              <Grid item xs>
                {/* <Link href="#" variant="body2">
                  Forgot password?
                </Link> */}
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
};

export default Login;
