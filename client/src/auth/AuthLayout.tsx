import { Outlet } from 'react-router';

const AuthLayout = () => {
  return <div >
    <section >
        
        <Outlet/>
    </section>
  </div>;
};

export default AuthLayout;