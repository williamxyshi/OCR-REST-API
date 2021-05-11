import { LockClosedIcon } from '@heroicons/react/solid'
import { useHistory } from "react-router-dom";
import {useState} from 'react'
import axios from 'axios'
import HeaderBar from './HeaderBar'
import Notification from './Notification'



export default function SignInPage({ setJwtToken, setUserModel }) {

  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  const [text, setText] = useState(false);

  const [show, setShow] = useState(false);

  const history = useHistory();

  const onForgot = ()=> {
    setText('haha too bad (for now)')
    setShow(true)
  }

  const handleSubmit= (e) => {
    const headers = {
      'Content-Type': 'application/json',
    }
    e.preventDefault();
    axios.post("http://3.22.225.249/api/user/login", {
      email: email,
      password: password
    }, {
      headers: headers
    }).then(res => {
      const jwt = res.data.token
      setJwtToken(jwt)
      axios.get("http://3.22.225.249/api/user").then(res => {
        setUserModel(res.data.user)
        history.push('/dashboard')
      })
    }).catch(e=>{
      setText('invalid email or password')
      setShow(true)
    })
  }

  return (
    <div>
    <Notification show={show} setShow={setShow} text={text}/>
    <HeaderBar />

    <div className="relative flex items-center justify-center bg-white py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">Sign in to your account</h2>
      
        </div>
        <form onSubmit={handleSubmit} className="mt-8 space-y-6">
          <input type="hidden" name="remember" defaultValue="true" />
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="email-address" className="sr-only">
                Email address
              </label>
              <input
                id="email-address"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm"
                placeholder="Email address"
                onChange={e=>setEmail(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-green-500 focus:border-green-500 focus:z-10 sm:text-sm"
                placeholder="Password"
                onChange={e=>setPassword(e.target.value)}
              />
            </div>
          </div>

          <div className="flex items-center justify-between">
       

            <div className="text-sm">
              <button onClick={onForgot} className="font-medium text-green-900 hover:text-red-500">
                Forgot your password?
              </button>
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
            >
              <span className="absolute left-0 inset-y-0 flex items-center pl-3">
                <LockClosedIcon className="h-5 w-5 text-green-500 group-hover:text-green-400" aria-hidden="true" />
              </span>
              Sign in
            </button>
          </div>
        </form>
      </div>
    </div>
    </div>
  )
}