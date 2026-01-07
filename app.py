from __future__ import annotations

import ipaddress
import os
from dataclasses import dataclass
from typing import Optional

from flask import Flask, render_template, request


app = Flask(__name__)


@dataclass
class ConversionResult:
    output: Optional[str] = None
    detail: Optional[list[str]] = None
    error: Optional[str] = None
    raw: Optional[str] = None


@dataclass
class CidrResult:
    cidr: Optional[str] = None
    network: Optional[str] = None
    broadcast: Optional[str] = None
    total: Optional[int] = None
    usable: Optional[int] = None
    first_host: Optional[str] = None
    last_host: Optional[str] = None
    error: Optional[str] = None
    raw: Optional[str] = None


def decimal_to_binary(ip_str: str) -> ConversionResult:
    result = ConversionResult(raw=ip_str)
    parts = ip_str.split(".")
    if len(parts) != 4:
        result.error = "Enter four decimal octets separated by dots."
        return result
    numbers = []
    for part in parts:
        if not part.isdigit():
            result.error = "Only digits and dots are allowed in decimal input."
            return result
        value = int(part)
        if value < 0 or value > 255:
            result.error = "Each decimal octet must be between 0 and 255."
            return result
        numbers.append(value)
    binaries = [format(value, "08b") for value in numbers]
    result.output = ".".join(binaries)
    result.detail = [
        f"Octet {index + 1}: {numbers[index]} → {binaries[index]}"
        for index in range(4)
    ]
    return result


def binary_to_decimal(binary_str: str) -> ConversionResult:
    result = ConversionResult(raw=binary_str)
    parts = binary_str.split(".")
    if len(parts) != 4:
        result.error = "Enter four binary octets separated by dots."
        return result
    if any(len(part) != 8 for part in parts):
        result.error = "Each binary octet must be exactly 8 bits."
        return result
    if any(set(part) - {"0", "1"} for part in parts):
        result.error = "Binary input may only include 0 and 1."
        return result
    numbers = [int(part, 2) for part in parts]
    result.output = ".".join(str(num) for num in numbers)
    result.detail = [
        f"Octet {index + 1}: {parts[index]} → {numbers[index]}"
        for index in range(4)
    ]
    return result


def cidr_to_hosts(cidr_str: str) -> CidrResult:
    result = CidrResult(raw=cidr_str)
    try:
        network = ipaddress.IPv4Network(cidr_str, strict=False)
    except ValueError:
        result.error = "Enter a valid IPv4 CIDR, e.g., 192.168.1.0/24."
        return result

    prefix = network.prefixlen
    total = network.num_addresses
    if prefix == 32:
        usable = 1
        first_host = str(network.network_address)
        last_host = str(network.network_address)
    elif prefix == 31:
        usable = 2
        first_host = str(network.network_address)
        last_host = str(network.broadcast_address)
    else:
        usable = max(total - 2, 0)
        first_host = (
            str(network.network_address + 1) if usable > 0 else "N/A"
        )
        last_host = (
            str(network.broadcast_address - 1) if usable > 0 else "N/A"
        )

    result.cidr = str(network.with_prefixlen)
    result.network = str(network.network_address)
    result.broadcast = str(network.broadcast_address)
    result.total = total
    result.usable = usable
    result.first_host = first_host
    result.last_host = last_host
    return result


@app.route("/", methods=["GET", "POST"])
def index():
    decimal_result = None
    binary_result = None
    cidr_result = None

    if request.method == "POST":
        action = request.form.get("action")
        if action == "decimal":
            raw = request.form.get("decimal_input", "").strip()
            decimal_result = decimal_to_binary(raw) if raw else None
        elif action == "binary":
            raw = request.form.get("binary_input", "").strip()
            binary_result = binary_to_decimal(raw) if raw else None
        elif action == "cidr":
            raw = request.form.get("cidr_input", "").strip()
            cidr_result = cidr_to_hosts(raw) if raw else None

    return render_template(
        "index.html",
        decimal_result=decimal_result,
        binary_result=binary_result,
        cidr_result=cidr_result,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(debug=True, port=port)
