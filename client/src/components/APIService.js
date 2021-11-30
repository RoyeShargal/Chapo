export default class APIService{
    // Insert a User
    static async InsertUser(body) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/signup`, {
                'method': 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(body)
            });
            return await response.json();
        } catch (error) {
            return console.log(error);
        }
    }

    //change password:
    static async InsertPassword(body) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/changepassword`, {
                'method': 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(body)
            });
            return await response.json();
        } catch (error) {
            return console.log(error);
        }
    }


    // insert post
    static async InsertPost(body) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/newpost`, {
                'method': 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(body)
            });
            return await response.json();
        } catch (error) {
            return console.log(error);
        }
    }

}