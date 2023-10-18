import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import MainView from './MainView';
import {createBrowserRouter,RouterProvider} from 'react-router-dom';

const router = createBrowserRouter([
  {
    path:"/",
    element: <MainView/>
  }
]);
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <RouterProvider router={router}/>
);