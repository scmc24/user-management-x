import './App.css';
import { Route, Routes } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {Snackbar, Alert} from '@mui/material'

import { authActions } from './store';
import { useEffect } from 'react';
import Header from './header/Header';
import Home from './home/Home';
import Register from './auth/Register';

import User from './clients/User';
import Login from './auth/Login';
import Profile from './clients/Profile';

function App() {
  const dispatch = useDispatch();
  const isLoggedIn = useSelector(state => state.isLoggedIn);
  const isAdmin = useSelector(state => state.isAdmin);
  console.log("is admin : ",isAdmin);
    // Get values from Redux store including the new snackbarId
    const openSnackbar = useSelector((state) => state.openSnackbar);
    const message = useSelector((state) => state.msg);
    const snackbarId = useSelector((state) => state.snackbarId);
  
    // Effect to auto-close Snackbar
    useEffect(() => {
      if (openSnackbar) {
        const timer = setTimeout(() => {
          dispatch(authActions.resetSnackbar());
        }, 3000);
  
        return () => clearTimeout(timer);
      }
    }, [snackbarId, dispatch]); // Dependencies include snackbarId
  
    const handleSnackbarClose = () => {
      dispatch(authActions.resetSnackbar());
    };
   
   // Update state based on changes in Redux store
   useEffect(() => {
     if(localStorage.getItem('token')) {
       dispatch(authActions.login());
     }
     if(localStorage.getItem('admin') === true ){
      console.log("set admin");
      dispatch(authActions.setAdmin());
     }
      
    
   }, [localStorage]); // Watch specific properties, not the entire cart object

  

   return (
     <div>
       <header>
         <Header />
       </header>
       <section>
         <Routes>
           <Route path="/" element={ isAdmin ? <Home /> : <Profile/>} />
           <Route path="/login" element={<Login />} />
           <Route path="/register" element={<Register />} />
           { (isLoggedIn && isAdmin) && <>
           <Route path="/clients" element={<User />} />
           </>
           
           }
           { isLoggedIn && <>
           <Route path="/profile" element={<Profile/>}/>
           
           </>
           
          }
           
         </Routes>
       </section>
       <section>
           <Snackbar 
                key={snackbarId} // Add key to force re-render
                open={openSnackbar}
                autoHideDuration={3000}
                onClose={handleSnackbarClose}
              >
                <Alert
                  onClose={handleSnackbarClose}
                  severity="success"
                  variant="filled"
                  sx={{ width: '100%' }}
                >
                  {message}
                </Alert>
              </Snackbar>
       </section>
     </div>
   );
}

export default App;
