from typing import Optional
from pydantic import BaseModel, Field
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler
from bson import ObjectId

# Compatibilité ObjectId pour Pydantic v2
class PyObjectId(ObjectId):
    """
    Classe personnalisée pour gérer les ObjectId de MongoDB avec Pydantic v2.
    Permet de valider et de convertir les chaînes en ObjectId.
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        return core_schema.no_info_after_validator_function(cls.validate, core_schema.str_schema())

    @classmethod
    def validate(cls, value):
        """
        Valide si la valeur est un ObjectId valide.
        Si la valeur n'est pas valide, une exception ValueError est levée.
        """
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return ObjectId(value)

class ProductModel(BaseModel):
    """
    Modèle Pydantic pour représenter un produit dans l'API Products.
    Utilise PyObjectId pour la compatibilité avec MongoDB.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True
    category: Optional[str] = None

    class Config:
        """
        Configuration du modèle Pydantic pour :
        - Utiliser les noms des champs pour la sérialisation JSON.
        - Encoder les ObjectId en chaînes de caractères.
        - Fournir un exemple de données pour la documentation.
        """
        populate_by_name = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Café Arabica",
                "description": "Café de haute qualité, origine Colombie",
                "price": 12.5,
                "in_stock": True,
                "category": "Boissons"
            }
        }
