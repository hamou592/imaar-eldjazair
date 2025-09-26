const express = require('express');
const nodemailer = require('nodemailer');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.json());

// Endpoint to handle email sending
app.post('/send-email', async (req, res) => {
    const { name, email, phone } = req.body;

    // Create a transporter
    const transporter = nodemailer.createTransport({
        service: 'gmail', // Use your email service
        auth: {
            user: 'nasreddinehamou8@gmail.com', // Replace with your email
            pass: 'Obtsp3114#', // Replace with your email password
        },
    });

    // Email options
    const mailOptions = {
        from: 'imaar-eldjazair@gmail.com',
        to: email,
        subject: 'Votre document PDF',
        text: `Bonjour ${name},\n\nMerci pour votre intérêt. Veuillez trouver ci-joint le document PDF.\n\nCordialement,\nImaar El Djazair`,
        attachments: [
            {
                filename: 'document.pdf',
                path: path.join(__dirname, 'document.pdf'), // Path to the PDF file
            },
        ],
    };

    try {
        await transporter.sendMail(mailOptions);
        res.status(200).send('Email sent successfully!');
    } catch (error) {
        console.error('Error sending email:', error);
        res.status(500).send('Failed to send email.');
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});