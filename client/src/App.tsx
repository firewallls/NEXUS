import { createBrowserRouter, RouterProvider} from 'react-router'
import AuthLayout from './auth/AuthLayout'
import SignIn from './auth/signin'
import SignUp from './auth/signup'
import Dashboard from './components/dashboard'
import { Navigate } from 'react-router';

function App() {
  const router = createBrowserRouter([
    {
      element: <AuthLayout />,
      children: [
        {
          path: '/signup',
          element: <SignUp />,
        },
        {
          path: '/signin',
          element: <SignIn />,
        }
      ]
    },
    {
    path: "/dashboard",
    element: <Dashboard />,
  },
  {
    path: "*",
    element: <Navigate to="/signin" replace />,
  }
  ])
  return (
    <>
      <RouterProvider router={router} />
    </>
  )
}

export default App