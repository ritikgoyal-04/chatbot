const express = require('express');
const mongoose = require('mongoose');
const path = require('path');
const bodyParser = require('body-parser');
const User = require('./models/User'); // Ensure this file exists

const app = express();
const PORT = 8000;

// Connect to MongoDB (Latest Syntax)
mongoose.connect('mongodb://127.0.0.1:27017/userAuth')
  .then(() => console.log("MongoDB connected"))
  .catch(err => console.log(err));


// Middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'views')));

// Serve frontend
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, 'views', 'index.html'));
});



// Signup Route
app.post("/signup", async (req, res) => {
    const { email, password } = req.body;
    try {
        const userExist = await User.findOne({ email });
        if (userExist) return res.status(400).json({ message: "User already exists" });

        const user = new User({ email, password });
        await user.save();
        res.status(201).json({ message: "User registered successfully" });
    } catch (error) {
        res.status(500).json({ message: "Something went wrong" });
    }
});

// Login Route
app.post("/login", async (req, res) => {
    const { email, password } = req.body;
    try {
        const user = await User.findOne({ email });
        if (!user) return res.status(400).json({ message: "Invalid credentials" });

        const isMatch = await user.comparePassword(password);
        if (!isMatch) return res.status(400).json({ message: "Not match" });

        // ✅ On successful login, redirect to Flask chatbot
        res.status(200).json({ redirectUrl: "http://127.0.0.1:5001" });
    } catch (error) {
        res.status(500).json({ message: "Something went wrong" });
    }
});

    

app.listen(PORT, () => console.log(`Server started at PORT: ${PORT}`));


// To run: npm start
// For database  manage: In command prompt  
// mongosh
// use userAuth
// show collections
// db.users.find().pretty()

// From the above four command you can see your user details 
// Login - ritikgoyal123@gmail.com
// Password - 12345
