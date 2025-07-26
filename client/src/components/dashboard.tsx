import { Button } from "../components/ui/button";
import { useEffect } from "react";
import { Link, useNavigate } from "react-router";

const Dashboard = () => {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  
  // Redirect to login if no session token
  useEffect(() => {
    if (!localStorage.getItem('session_token')) {
      navigate('/signin');
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('session_token');
    localStorage.removeItem('user');
    navigate('/signin');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md p-8 bg-white rounded-lg shadow-lg">
        <div className="text-center mb-8">
          <div className="mx-auto bg-gray-200 border-2 border-dashed rounded-xl w-16 h-16 mb-4" />
          <h1 className="text-2xl font-bold">Welcome, {user.name || 'User'}!</h1>
          <p className="text-gray-600">You're successfully authenticated</p>
        </div>
        
        <div className="space-y-4 mb-8">
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">Email Address</p>
            <p className="font-medium">{user.email}</p>
          </div>
          
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">Session Status</p>
            <p className="font-medium text-green-600">Active</p>
          </div>
        </div>
        
        <Button 
          onClick={handleLogout}
          className="w-full bg-red-600 hover:bg-red-700"
        >
          Logout
        </Button>
        
        <div className="mt-6 text-center text-sm text-gray-600">
          <p>Need help? <a href="#" className="text-blue-600 hover:underline">Contact support</a></p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;