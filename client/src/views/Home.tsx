import React from 'react'

interface HomeProps {
    token: string | null
}

function Home({ token }: HomeProps) {
    return (
        <div>
            <h1>This is the home page!</h1>
            {token && <p>{token}</p>}
        </div>
    )
}

export default Home
