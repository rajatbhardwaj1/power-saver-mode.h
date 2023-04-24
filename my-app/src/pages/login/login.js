import React from "react";
import "./login.css"

function Login()
{
    return(
        <div>
            <div class="login-container">
                <h2>Login</h2>
                <form>
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username"/>
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password"/>
                    <input type="submit" value="Submit"></input>
                </form>
            </div>
        </div>
        )
}
export default Login;