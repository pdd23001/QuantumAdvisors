const express = require("express");
const app = express();

app.use(express.json());
const studentdata = require("./studentdata.json");

app.get("/", (req, res) => {
    res.json({ message: "Home page" });
});

app.get("/classes/:id", (req, res) => {
    let id = req.params.id;
    res.json(studentdata.students[id]);
});

// Start server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});