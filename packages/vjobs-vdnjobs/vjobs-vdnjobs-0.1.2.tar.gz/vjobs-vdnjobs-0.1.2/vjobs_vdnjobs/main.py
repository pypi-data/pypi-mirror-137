import os
from urllib.parse import urljoin

import swagger_client
import virden_jobs.common.job


def _get_jobs():
    configuration = swagger_client.Configuration()
    configuration.username = os.environ['VDNJOBS_USERNAME']
    configuration.password = os.environ['VDNJOBS_PASSWORD']
    api_instance = swagger_client.JobsApi(swagger_client.ApiClient(configuration))    
    api_response = api_instance.jobs_list(lasthours=24)

    lst = []
    for job in api_response.results:
        company = job.unverified_company
        if job.company:
            company = job.company
        url = urljoin('https://vdnjobs.ca/job/', job.id)
        vjob = virden_jobs.common.job.Job(job.name, url, company=company)
        lst.append(vjob)
    return lst


def run():
    return _get_jobs()
