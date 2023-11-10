const express= require('express')
const fs = require('fs');
const router = express.Router()
const xlsx = require('xlsx');

// Read data from excel
const excelFilePath = './Data/Demo_Unified_Dashboard_Data_2023.xlsx';
const workbook  = xlsx.readFile(excelFilePath);

const sheetName = workbook.SheetNames[0];
const worksheet = workbook.Sheets[sheetName];

const data = xlsx.utils.sheet_to_json(worksheet);
// Read Data End from excel


// Python script for GenAI - start
// const ques = 'count of country from column Country?'

const { spawn } = require('child_process');
const path = require('path')



// const pythonProcess = spawn('python', [pythonScriptPath,ques]);

// pythonProcess.stdout.on('data', (data) => {
//     console.log(`Python Script Output: ${data}`);
//   });

// pythonProcess.stderr.on('data', (data) => {
// console.error(`Python Script Error: ${data}`);
// });

// pythonProcess.on('close', (code) => {
// console.log(`Python Script Exited with Code: ${code}`);
// });

console.log(__dirname)

// Python script for GenAI - end


/**
 * @swagger
 * components:
 *  schemas:
 *   VirutalAgentAPI:
 *    type: object
 *    required:
 *     - name
 *    properties:
 *     name:
 *      type: string
 *      description: Enter Name
 */

/**
 * @swagger
 * tags:
 *  name:   VirutalAgentAPI
 *  description:    API to connect powerBI and Virutal aggent
 */

/**
 * @swagger
 * /getData:
 *  get:
 *   summary: Table Data
 *   responses:
 *    200:
 *      description:    Server Informaiton
 *      content:
 *       application/json:
 *        schema:
 *         type:    object
 *         properties:
 *          name:
 *           type:  string
 */
router.get('/getData',(req,res)=>{
    // res.end("From Server")
    res.json(data)
})


/**
 * @swagger
 * /askQuestion:
 *  post:
 *   summary:   Get the response from table using OPenAI
 *   tags:  [VirutalAgentAPI]
 *   requestBody:
 *    content: 
 *     application/json:   
 *      schema:
 *       type:  object
 *       properties:
 *        question:
 *         type:    string
 *         description: The question to be sent
 *      
 *   responses:
 *    200:
 *     description: Response from Open API
 *     content:
 *      application/json:
 *       schema:
 *        type: object
 *       
 *       
 */
router.post('/askQuestion',(req,res)=>{
    console.log(req.body['Question']);
    const ques = req.body['Question']

    const pythonScriptPath = path.join(__dirname,'../GenAI/IBM_GenAI.py')
    const pythonProcess = spawn('python', [pythonScriptPath,ques]);

    let data = ''
    pythonProcess.stdout.on('data', (chunk) => {
        data += chunk.toString();
        console.log(`Python Script Output: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python Script Exited with Code: ${code}`);
        // Send the collected data as the response when the Python script is done
        let jsonData = JSON.parse(data);
        res.json({ question: `Your question ${ques}`, data: jsonData });
        
    });
   
})



module.exports = router;