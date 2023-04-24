import React from "react";
import "./create_account.css"

function CreateAccount()
{
    return(
        <div>
            <div class="login-container">
                <h2>Create Account</h2>
                <form>
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username"/>

                    <label for="name">Name:</label>
                    <input type="text" id="Name" name="Name"/>


                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password"/>

                    <input type="submit" value="Submit"></input>
                </form>
            </div>
        </div>
        )
}
export default CreateAccount;