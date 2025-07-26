import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "../components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "../components/ui/form";
import { Input } from "../components/ui/input";
import { useState } from "react";
import { Link, useNavigate } from "react-router";

type FormType = 'signin' | 'signup';

// Create a function to generate the schema based on the form type
const AuthFormSchema = (type: FormType) => {
  return z.object({
    fullName: type === 'signup' ? z.string().min(2, "Minimum 2 characters").max(50) : z.string().optional(),
    email: z.string().email("Please enter a valid email address"),
    otp: z.string().optional()
  })
}

const AuthForm = ({ type }: { type: FormType }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [showOTP, setShowOTP] = useState(false);
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  
  const navigate = useNavigate();
  
  const formSchema = AuthFormSchema(type);
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      fullName: "",
      email: "",
      otp: ""
    },
  });

  const API_URL = import.meta.env.VITE_API_URL ;

  // Handle initial form submission (signup/login)
  const handleInitialSubmit = async (values: z.infer<typeof formSchema>) => {
    setIsLoading(true);
    setErrorMessage('');
    
    try {
      // Save email and full name for later use
      setEmail(values.email);
      if (type === 'signup') {
        setFullName(values.fullName || '');
      }
      
      // Determine endpoint based on form type
      const endpoint = type === 'signin' ? "/login" : "/signup";
      
      // Prepare payload
      const payload = type === 'signup' 
        ? { name: values.fullName, email: values.email } 
        : { email: values.email };
      
      // Call backend API
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: "POST",
        body: JSON.stringify(payload)
      });

      let result: Record<string, unknown> = {};
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        result = await response.json();
      }

      if (response.ok) {
        setShowOTP(true);
      } else {
        setErrorMessage(typeof result.detail === "string" ? result.detail : "An error occurred");
      }
    } catch (error: unknown) {
      if (error instanceof Error) {
        setErrorMessage(error.message || "Network error");
      } else {
        setErrorMessage("Network error");
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Handle OTP verification
  const handleOTPSubmit = async (otp: string) => {
    setIsLoading(true);
    setErrorMessage('');
    
    try {
      const response = await fetch(`${API_URL}/verify-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: email,
          otp: otp
        })
      });

      let result: Record<string, unknown> = {};
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        result = await response.json();
      }

      if (response.ok) {
        localStorage.setItem('session_token', String(result.session_token));
        localStorage.setItem('user', JSON.stringify({
          name: fullName || '',
          email: email
        }));
        navigate('/dashboard');
      } else {
        setErrorMessage(typeof result.detail === "string" ? result.detail : "Invalid OTP");
      }
    } catch (error: unknown) {
      if (error instanceof Error) {
        setErrorMessage(error.message || "Network error");
      } else {
        setErrorMessage("Network error");
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Form submission handler
  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    if (showOTP) {
      // Handle OTP submission
      await handleOTPSubmit(values.otp || '');
    } else {
      // Handle initial submission
      await handleInitialSubmit(values);
    }
  };

  return (
    <div className="w-full max-w-md p-8 bg-white rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold text-center mb-6">
        {type === 'signin' ? 'Sign In' : 'Create Account'}
      </h1>
      
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          {!showOTP ? (
            <>
              {type === 'signup' && (
                <FormField
                  control={form.control}
                  name="fullName"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Full Name</FormLabel>
                      <FormControl>
                        <Input 
                          placeholder="Enter your full name" 
                          {...field} 
                          disabled={isLoading}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              )}
              
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Email Address</FormLabel>
                    <FormControl>
                      <Input
                        type="email"
                        placeholder="Enter your email"
                        {...field}
                        disabled={isLoading}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </>
          ) : (
            <FormField
              control={form.control}
              name="otp"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Verification Code</FormLabel>
                  <FormControl>
                    <Input
                      type="text"
                      placeholder="Enter 6-digit code"
                      maxLength={6}
                      {...field}
                      disabled={isLoading}
                    />
                  </FormControl>
                  <p className="text-sm text-gray-500 mt-2">
                    We've sent a verification code to your email
                  </p>
                  <FormMessage />
                </FormItem>
              )}
            />
          )}
          
          <Button 
            type="submit" 
            className="w-full"
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </span>
            ) : showOTP ? (
              'Verify Code'
            ) : type === 'signin' ? (
              'Sign In'
            ) : (
              'Create Account'
            )}
          </Button>
          
          {errorMessage && (
            <div className="p-3 bg-red-50 text-red-700 rounded-md">
              <p className="font-medium">Error:</p>
              <p>{errorMessage}</p>
            </div>
          )}

          {!showOTP && (
            <div className="text-center text-sm text-gray-600">
              <p>
                {type === 'signin' ? "Don't have an account?" : "Already have an account?"}{' '}
                <Link 
                  to={type === 'signin' ? '/signup' : '/signin'} 
                  className="font-medium text-blue-600 hover:text-blue-800"
                >
                  {type === 'signin' ? 'Sign Up' : 'Sign In'}
                </Link>
              </p>
            </div>
          )}
        </form>
      </Form>
      
      {showOTP && (
        <div className="mt-4 text-center">
          <button 
            onClick={() => setShowOTP(false)}
            className="text-sm text-blue-600 hover:text-blue-800"
          >
            Change Email
          </button>
        </div>
      )}
    </div>
  );
};

export default AuthForm;