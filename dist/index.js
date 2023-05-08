"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const axios_1 = __importDefault(require("axios"));
const jsdom_1 = require("jsdom");
const dotenv_1 = __importDefault(require("dotenv"));
dotenv_1.default.config();
const proxyConfig = {
    host: 'zproxy.lum-superproxy.io',
    port: 22225,
    auth: {
        username: process.env.luminatiUsername,
        password: process.env.luminatiPassword,
    },
};
async function getHTML(url) {
    const response = await axios_1.default.get(url, {
        proxy: proxyConfig,
        headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
        },
    });
    return response.data;
}
async function parseDoctorsList(page) {
    const url = `https://www.idf.co.uk/patients/find-a-doctor.aspx?Specialty=20&SubSpecialty=0&AreaCode=W1G&SearchCriteria=London&PageNumber=${page}`;
    const html = await getHTML(url);
    const doctors = [];
    const dom = new jsdom_1.JSDOM(html);
    const anchorElements = dom.window.document.querySelectorAll('.doctor-list .doctor-details a');
    anchorElements.forEach((element) => {
        if (element.hasAttribute('href')) {
            doctors.push(element.getAttribute('href'));
        }
    });
    return doctors;
}
async function main() {
    const doctorsList = await parseDoctorsList(1);
    console.log(doctorsList);
}
main();
//# sourceMappingURL=index.js.map