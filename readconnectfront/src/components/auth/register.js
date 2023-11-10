import React from "react";

class Register extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            registrationEmail: "",
            registrationUsername: "",
            registrationPassword: "",
            registrationSuccess: false,
        };
        this.handleRegister = this.handleRegister.bind(this);
    }

    handleRegister(e) {
        e.preventDefault();
        fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: this.state.registrationUsername,
                password: this.state.registrationPassword,
                email: this.state.registrationEmail,
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                if (data.success) {
                    this.setState({ registrationSuccess: true });
                }
            })
            .catch((error) => {
                console.error(error);
            });
    }

    render() {
        return (
            <div className="register">
                <h2>Register</h2>
                <form onSubmit={this.handleRegister}>
                    <label>
                        Nombre de Usuario:
                        <input
                            type="text"
                            value={this.state.registrationUsername}
                            onChange={(e) => this.setState({ registrationUsername: e.target.value })}
                        />
                    </label>
                    <label>
                        Contraseña:
                        <input
                            type="password"
                            value={this.state.registrationPassword}
                            onChange={(e) => this.setState({ registrationPassword: e.target.value })}
                        />
                    </label>
                    <label>
                        Email:
                        <input
                            type="email"
                            value={this.state.registrationEmail}
                            onChange={(e) => this.setState({ registrationEmail: e.target.value })}
                        />
                    </label>
                    <button type="submit">Register</button>
                </form>
                {this.state.registrationSuccess && <p>Registration successful!</p>}
            </div>
        );
    }
}

export default Register;
