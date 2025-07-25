import { z } from "zod"
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Button } from "../components/ui/button"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "../components/ui/form"
import { Input } from "../components/ui/input"
import { useState } from "react";
import { Link } from "react-router";


type formtype = 'signin' | 'signup';
// Create a function to generate the schema based on the form type
const AuthFormSchema = (type : formtype) => {
  return z.object({
    FullName : type === 'signup' ? z.string().min(2).max(50) : z.string().optional(),
    Phone_no: z.number().min(10).max(10),
  })
}


const AuthForm = ({type} : {type: formtype}) => {
    const [isloading] = useState(false); // setIsLoading
    const [errorMessage] = useState(''); // setErrorMessage
    const formSchema = AuthFormSchema(type);
    const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
        FullName: "",
        Phone_no: undefined,
    },
    });

    // 2. Define a submit handler.
    const onSubmit = async (values: z.infer<typeof formSchema>) =>{
        console.log(values)
    };

    return (<>
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} >
        <h1 > {type === 'signin' ? 'Sign In' : 'Sign Up'} </h1>
        {type === 'signup' && <FormField
          control={form.control}
          name="FullName"
          render={({ field }) => (
            <FormItem>
                <div > 
                    <FormLabel >Full name</FormLabel>
                    <FormControl>
                        <Input placeholder="Enter your full name" {...field} />
                    </FormControl>
                </div>

              <FormMessage />
            </FormItem>
          )}
        />
        }
        <FormField
          control={form.control}
          name="Phone_no"
          render={({ field }) => (
            <FormItem>
                <div > 
                    <FormLabel >Phone Number</FormLabel>
                    <FormControl>
                        <Input placeholder="Enter your number" {...field} />
                    </FormControl>
                </div>

              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" disabled={isloading}>
            {type === 'signin' ? 'Sign In' : 'Sign Up'}
            {isloading && (
                <img src="../assets/icons/loader.svg" alt="loader" width={24} height={24} />
            )}
        </Button>
        
        {errorMessage && <p className="error-message">*{errorMessage}</p>}

        <div >
          <p >
            {type === 'signin' ? 'Don\'t have an account?' : 'Already have an account?'}
          </p>
          <Link to={type === 'signin' ? '/signup' : '/signin'}>
            {type === 'signin' ? 'Sign Up' : 'Sign In'}
          </Link>

        </div>
      </form>
    </Form>
    {/* otp authorization */}
    </>
  )
    };

export default AuthForm;