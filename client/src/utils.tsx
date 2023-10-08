export const setSafeCookie = (
    cookie: string,
    cookieName: string,
    hoursToExpiry: number
) => {
    let date = new Date()
    date.setHours(date.getHours() + hoursToExpiry)
    document.cookie = `${cookieName}=${cookie}; expires=${date.toUTCString()}; path=/;` // TODO: add "samesite=strict; secure; HttpOnly"
}

export const getCookie = (cookieName: string) => {
    const cookie = document.cookie
        .split('; ')
        .find((row) => row.startsWith(`${cookieName}=`))
        ?.split('=')[1]

    console.log(cookie)
}
