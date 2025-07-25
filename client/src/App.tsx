import { createBrowserRouter, RouterProvider} from 'react-router'
import AuthLayout from './auth/AuthLayout'
import SignIn from './auth/signin'
import SignUp from './auth/signup'

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
    }
  ])
  return (
    <>
      <RouterProvider router={router} />
    </>
  )
}

export default App