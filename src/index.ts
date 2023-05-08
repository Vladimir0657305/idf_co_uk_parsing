import axios, { AxiosProxyConfig } from 'axios';
import { JSDOM } from 'jsdom';
import dotenv from 'dotenv';

dotenv.config();

const proxyConfig: AxiosProxyConfig = {
    host: 'zproxy.lum-superproxy.io',
    port: 22225,
    auth: {
        username: process.env.luminatiUsername!,
        password: process.env.luminatiPassword!,
    },
};

async function getHTML(url: string): Promise<string> {
    const response = await axios.get(url, {
        proxy: proxyConfig,
        headers: {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
        },
    });

    return response.data;
}

async function parseDoctorsList(page: number): Promise<string[]> {
    const url = `https://www.idf.co.uk/patients/find-a-doctor.aspx?Specialty=20&SubSpecialty=0&AreaCode=W1G&SearchCriteria=London&PageNumber=${page}`;

    const html = await getHTML(url);
    const doctors: string[] = [];

    const dom = new JSDOM(html);
    const anchorElements = dom.window.document.querySelectorAll('.doctor-list .doctor-details a');

    anchorElements.forEach((element) => {
        if (element.hasAttribute('href')) {
            doctors.push(element.getAttribute('href')!);
        }
    });

    return doctors;
}

async function main() {
    const doctorsList = await parseDoctorsList(1);
    console.log(doctorsList);
}

main();
