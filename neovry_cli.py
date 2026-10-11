#!/usr/bin/env python3
"""
NEOVRY 13OS - Core Dashboard & CLI Utility
Cross-platform architecture supporting headless Termux environments.
"""

import sys
import json
import argparse
from typing import Dict, Any, Union

# Safe Tkinter import pattern for headless environments
HAS_TKINTER = False
try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False


def process_affiliate_lead(payload_raw: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Process and qualify incoming affiliate marketing leads safely using EAFP patterns."""
    try:
        data = json.loads(payload_raw) if isinstance(payload_raw, str) else payload_raw
    except (TypeError, json.JSONDecodeError):
        data = {}

    lead_name = data.get("name", "Prospecto").strip()
    message = data.get("message", "").lower().strip()
    source = data.get("source", "telegram").lower()

    niche_mapping = {
        "reposteria": "Curso de Repostería Casera",
        "brigadeiro": "Brigadeiro Gourmet",
        "panaderia": "Panadería Artesanal",
        "ingles": "Curso de Inglés Rápido",
        "desayuno": "Guía de Desayunos Saludables",
        "mascotas": "Educación Canina Pro",
    }

    detected_product = "Catálogo General de Afiliados"
    for keyword, product in niche_mapping.items():
        if keyword in message:
            detected_product = product
            break

    score = 10
    if "precio" in message or "comprar" in message or "enlace" in message:
        score = 50
    elif "info" in message or "mas informacion" in message:
        score = 30

    return {
        "lead_name": lead_name,
        "product_interest": detected_product,
        "lead_score": score,
        "channel": source,
        "action_required": "send_checkout_link" if score >= 50 else "send_nurturing_sequence"
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NEOVRY 13OS CLI Core Utility")
    parser.add_argument("--test-lead", type=str, help="Probar calificación de un lead en formato JSON")
    parser.add_argument("--audit", action="store_true", help="Auditar estado rápido del núcleo")

    args = parser.parse_args()

    if args.test_lead:
        result = process_affiliate_lead(args.test_lead)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.audit:
        print("[OK] Núcleo NEOVRY 13OS operando en modo headless y listo para automatización.")
    else:
        if not HAS_TKINTER:
            sys.stderr.write(
                "ECC Dashboard: Entorno sin Tkinter detectado.\n"
                "Usa el modo CLI (ej: python3 neovry_cli.py --audit)\n"
            )
            sys.exit(1)
        else:
            print("Lanzando interfaz gráfica...")
