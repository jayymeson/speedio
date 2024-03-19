from fastapi import APIRouter, HTTPException, status
from models.model import SiteInfo, SaveInfoRequest
from database.mongodb import collection_name
from schema.serializer import serializer
from database.headers import headersNoAuth
from pydantic import BaseModel
import requests
import json

router = APIRouter()

class UrlRequestBody(BaseModel):
    url: str

@router.post("/get_info")
async def get_info_POST(request_body: UrlRequestBody):
    site = collection_name.find_one({"url": request_body.url})
    if site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return serializer(site)

@router.post("/save_info")
async def save_info(request: SaveInfoRequest):
    url = request.url
    noAuth_url = f'https://data.similarweb.com/api/v1/data?domain={url}'
    responseNoAuth = requests.get(noAuth_url, headers=headersNoAuth)
    
    if responseNoAuth.status_code == 200:
        dataNoAuth = json.loads(responseNoAuth.text)
        
        siteInfo: SiteInfo = {
            "url": url,
            "siteName": dataNoAuth['SiteName'],
            "classification": {
                "GlobalRank": dataNoAuth['GlobalRank']['Rank'] if dataNoAuth['GlobalRank']['Rank'] is not None else 0,
                "CountryRank": dataNoAuth['CountryRank']['Rank'] if dataNoAuth['CountryRank']['Rank'] is not None else 0,
                "CategoryRank": int(dataNoAuth['CategoryRank']['Rank']) if dataNoAuth['CategoryRank']['Rank'] is not None else 0
            },
            "category": dataNoAuth['Category'],
            "average_visit_duration": str(float(dataNoAuth['Engagments']['TimeOnSite']) / 60),
            "pages_per_visit": dataNoAuth['Engagments']['PagePerVisit'],
            "bounce_rate": str(float(dataNoAuth['Engagments']['BounceRate']) * 100) + "%",
            "top_countries": dataNoAuth['TopCountryShares'],
            "gender_distribution": None, 
            "age_distribution": None, 
            "competitors": dataNoAuth.get('Competitors', {'TopSimilarityCompetitors': []}),
            "keywords": dataNoAuth.get('TopKeywords', [])
        }
        
        collection_name.insert_one(siteInfo)
        return {"message": "Informação salva com sucesso!", "status": status.HTTP_201_CREATED}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foi possível obter os dados para a URL fornecida.")
