# Implementation of API Routes

This directory contains the definitions of all available API endpoints. The definition of endpoints is the most essential aspect of an interface, and in this project, each endpoint is implemented within its respective subfolder in this directory.

## Folder Structure

The folder structure is designed to mirror the paths of the endpoints. For example, both `/expertise` and `/expertise/{id}` are implemented within the [./expertise](./expertise/) folder. This structure ensures good orientation, maintainability, and transparency throughout the codebase.

## Purpose

The goal is to keep business logic out of the endpoint implementations as much as possible. Instead, business logic should be handled in the [Services](../../services/) layer and through database access helpers in [../db/queries/](../../db/queries/) using queries. The focus within the endpoint implementations should be on error handling and managing the interface between the client and the backend.