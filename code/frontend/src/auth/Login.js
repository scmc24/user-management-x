import React, { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  CircularProgress,
  Alert,
} from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { login } from '../api-endpoints/endpoints';
import { authActions } from '../store';

const Login = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [inputs, setInputs] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Handle login response
  const onResReceived = (data) => {
    console.log(data);
    localStorage.setItem('userId', data.data.user.id);
    localStorage.setItem('token', data.data.token);
    localStorage.setItem('email', data.data.user.email);
    localStorage.setItem('username', data.data.user.username);
    localStorage.setItem('admin', data.data.user.is_superuser);

    dispatch(authActions.login());
    if (data.data.user.is_superuser) {
      console.log("setting admin");
      dispatch(authActions.setAdmin());
    }
    navigate('/');
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    login(inputs)
      .then(onResReceived)
      .catch((err) => {
        console.error(err);
        setError('Invalid email or password. Please try again.');
      })
      .finally(() => setLoading(false));
  };

  // Handle input change
  const handleChange = (e) => {
    setInputs((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  return (
    <Box
      width={{ xs: '90%', sm: '40%' }}
      borderRadius={4}
      boxShadow={'0px 4px 20px rgba(0, 0, 0, 0.1)'}
      margin={'auto'}
      marginTop={{ xs: 4, sm: 8 }}
      sx={{ backgroundColor: 'background.paper' }}
    >
      <form onSubmit={handleSubmit}>
        <Box
          display={'flex'}
          flexDirection={'column'}
          width={'80%'}
          padding={3}
          margin={'auto'}
        >
          {/* Title */}
          <Typography
            fontFamily={'quicksand'}
            padding={2}
            variant="h4"
            color="primary"
            textAlign={'center'}
            fontWeight="bold"
            sx={{ mb: 2 }}
          >
            Login
          </Typography>

          {/* Error Message */}
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {/* Email Field */}
          <TextField
            label="Email"
            value={inputs.email}
            onChange={handleChange}
            name="email"
            type="email"
            required
            margin="normal"
            fullWidth
            sx={{ mb: 2 }}
          />

          {/* Password Field */}
          <TextField
            label="Password"
            value={inputs.password}
            onChange={handleChange}
            name="password"
            type="password"
            required
            margin="normal"
            fullWidth
            sx={{ mb: 2 }}
          />

          {/* Login Button */}
          <Button
            sx={{
              mt: 2,
              borderRadius: 2,
              padding: 1.5,
              backgroundColor: 'primary.main',
              color: 'white',
              '&:hover': {
                backgroundColor: 'primary.dark',
              },
            }}
            type="submit"
            variant="contained"
            disabled={loading}
            fullWidth
          >
            {loading ? <CircularProgress size={24} color="inherit" /> : 'Login'}
          </Button>

          {/* Signup Link */}
          <Typography
            variant="body2"
            textAlign={'center'}
            sx={{ mt: 2, color: 'text.secondary' }}
          >
            Don't have an account?{' '}
            <Button
              component={Link}
              to="/register"
              variant="text"
              color="primary"
              sx={{ textTransform: 'none', p: 0 }}
            >
              Signup
            </Button>
          </Typography>
        </Box>
      </form>
    </Box>
  );
};

export default Login;