import json
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import DiagnosticoCreate, DiagnosticoOut
from model import Diagnostico
from auth import get_db, obter_usuario_atual
from servicos.rede_bayesianas import criar_rede_bayesiana
from pgmpy.inference import VariableElimination

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/diagnostico", tags=["diagnostico"])

# Mapeamento dos sintomas do frontend para os nomes da rede
SINTOMAS_MAP = {
    'febre': 'Febre',
    'diarreia': 'Diarreia',
    'fadiga': 'Fadiga',
    'vomito': 'Vomito',
    'dorUrinaria': 'DorUrinaria'
}

VALID_NODES = {'Febre', 'Diarreia', 'Fadiga', 'Vomito', 'DorUrinaria'}

@router.post("", response_model=DiagnosticoOut)
def diagnosticar(
    diagnostico: DiagnosticoCreate,
    db: Session = Depends(get_db),
    usuario = Depends(obter_usuario_atual)
):
    try:
        # 1. Receber e normalizar os sintomas
        sintomas = diagnostico.sintomas
        sintomas_normalizados = {
            SINTOMAS_MAP.get(k, k): int(v) if v is not None else None
            for k, v in sintomas.items()
        }

        # 2. Criar modelo e inicializar inferência
        model = criar_rede_bayesiana()
        inference = VariableElimination(model)

        # 3. Preparar evidência
        evidencia = {
            k: v for k, v in sintomas_normalizados.items()
            if k in VALID_NODES and v in {0, 1}
        }

        # 4. Detectar automaticamente os nós de doenças
        doencas = [
            cpd.variable
            for cpd in model.get_cpds()
            if len(cpd.get_evidence()) > 0
        ]
        logger.debug(f"Doenças detectadas: {doencas}")

        # 5. Realizar inferência para cada doença
        resultado = {}
        for doenca in doencas:
            try:
                query = inference.query(variables=[doenca], evidence=evidencia)
                resultado[doenca.lower()] = float(query.values[1])  # P(doenca=1)
            except Exception as e:
                logger.warning(f"Falha ao inferir {doenca}: {e}")

        # 6. Armazenar no banco
        db_diagnostico = Diagnostico(
            usuario_id=usuario.id,
            sintomas=json.dumps(sintomas),
            resultado=json.dumps(resultado)
        )
        db.add(db_diagnostico)
        db.commit()
        db.refresh(db_diagnostico)

        # 7. Retornar resultado
        return DiagnosticoOut(
            id=db_diagnostico.id,
            sintomas=json.loads(db_diagnostico.sintomas),
            resultado=json.loads(db_diagnostico.resultado),
            data=db_diagnostico.data
        )

    except Exception as e:
        logger.error(f"Erro ao criar diagnóstico: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor.")

historico_router = APIRouter(prefix="/historico", tags=["historico"])

@historico_router.get("/")
def listar_historico(usuario=Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    try:
        historico = db.query(Diagnostico)\
            .filter(Diagnostico.usuario_id == usuario.id)\
            .order_by(Diagnostico.data.desc())\
            .all()
        
        return [
            {
                "id": d.id,
                "sintomas": json.loads(d.sintomas),
                "resultado": json.loads(d.resultado),
                "data": d.data.isoformat()
            }
            for d in historico
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao carregar histórico")
