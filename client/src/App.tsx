import React, { useEffect, useState } from 'react'
import {
    createBrowserRouter,
    createRoutesFromElements,
    Route,
    RouterProvider,
} from 'react-router-dom'
import logo from './logo.svg'
import './App.css'
import { Root, Authentication, Home } from './views'

const isAuth = false // TODO: use to conditionally render Auth page

function App() {
    const [token, setToken] = useState<string | null>(null)

    // useEffect(() => {
    //     fetch('http://127.0.0.1:8000/api/user/1', {
    //         method: 'GET',
    //         mode: 'cors',
    //     })
    //         .then((response) => response.json())
    //         .then((data) => {
    //             console.log(data)
    //         })
    //         .catch((error) => {
    //             console.error(error)
    //         })
    // }, [])

    const sourceJWT = () => {
        // Check for JWT in local storage
    }

    const router = createBrowserRouter(
        createRoutesFromElements(
            <Route path='/' element={<Root />}>
                <Route index element={<Home token={token} />} />
                <Route
                    path='/auth'
                    element={<Authentication setToken={setToken} />}
                />
            </Route>
        )
    )

    return (
        <div className='App'>
            <RouterProvider router={router} />
            <button
                onClick={() => {
                    console.log(`token from App.tsx click: ${token}`)
                }}
            />
        </div>
    )
}

export default App
