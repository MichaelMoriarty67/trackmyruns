import React, { useEffect, useState } from 'react'
import { initializeApp } from 'firebase/app'
import { getAnalytics } from 'firebase/analytics'
import {
    getAuth,
    createUserWithEmailAndPassword,
    Auth,
    User,
    signInWithEmailAndPassword,
    IdTokenResult,
} from 'firebase/auth'
import { setSafeCookie, getCookie } from '../utils'
import axios from 'axios'

// TODO: make firebase config and methods into a custom hook (?)
const firebaseConfig = {
    apiKey: 'AIzaSyCQYU5F0gDGDRh5j7qxQEfbUu8FAP758uk',
    authDomain: 'trackmyruns8.firebaseapp.com',
    projectId: 'trackmyruns8',
    storageBucket: 'trackmyruns8.appspot.com',
    messagingSenderId: '489616088135',
    appId: '1:489616088135:web:3849d1a22cccc590b62562',
    measurementId: 'G-ZEG2SL857Z',
}

// Initialize Firebase
const app = initializeApp(firebaseConfig)
const auth = getAuth(app)

let email = 'm.hockey8@gmail.com'
let password = 'test_password_1'

interface AuthData {
    email: string
    password: string
}

interface AuthenticationProps {
    setToken(token: string): void
}

const test_auth = () => {
    axios
        .get('http://localhost:8000/api/runs', {
            // must call localhost; 127.0.0.1 won't send cookies
            method: 'GET',
            withCredentials: true,
        })
        .then((response) => {
            console.log(response)
        })
        .catch((error) => {
            console.error(error)
        })
}

function Authentication({ setToken }: AuthenticationProps) {
    const [user, setUser] = useState<User | null>(null)
    const [errorMessage, setErrorMessage] = useState<string | null>(null)

    const handleUserCreation = (auth: Auth, credentials: AuthData) => {
        createUserWithEmailAndPassword(
            auth,
            credentials.email,
            credentials.password
        )
            .then((user) => {
                setUser(user.user)
                user.user.getIdTokenResult().then((tokenId: IdTokenResult) => {
                    setSafeCookie(tokenId.token, 'firebase_token', 1)
                    setToken(tokenId.token)
                })
            })
            .catch((error) => {
                console.error(
                    `Error code during createUserWithEmailAndPassword: ${error}`
                )
                setErrorMessage(error.message)
            })
    }

    const handleUserSignIn = (auth: Auth, credentials: AuthData) => {
        signInWithEmailAndPassword(
            auth,
            credentials.email,
            credentials.password
        )
            .then((user) => {
                setUser(user.user)
                user.user.getIdTokenResult().then((tokenId: IdTokenResult) => {
                    setSafeCookie(tokenId.token, 'firebase_token', 1)
                    setToken(tokenId.token)
                })
            })
            .catch((error) => {
                console.error(
                    `Error code during createUserWithEmailAndPassword: ${error}`
                )
                setErrorMessage(error.message)
            })
    }

    useEffect(() => {
        // check for JWT and sign in with it if avail
    })

    return (
        <div>
            <h1>Auth page going here!</h1>
            <button
                onClick={() => handleUserCreation(auth, { email, password })}
            >
                {' '}
                Sign Up{' '}
            </button>
            <button onClick={() => handleUserSignIn(auth, { email, password })}>
                {' '}
                Sign In{' '}
            </button>
            <button onClick={() => getCookie('firebase_token')}>
                {' '}
                Get Cookie{' '}
            </button>
            <button onClick={test_auth}> Call Auth </button>

            {errorMessage && <p>Error: {errorMessage}</p>}
        </div>
    )
}

export default Authentication
