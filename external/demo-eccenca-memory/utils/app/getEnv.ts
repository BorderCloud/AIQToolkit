// utils/app/getEnv.ts

/**
 * getEnv - récupère une variable d'environnement avec validation.
 * Lance une erreur si la variable est manquante.
 */
export function getEnv(key: string): string {
  const value = process.env[key];
  if (typeof value === 'undefined' || value === '') {
    throw new Error(`❌ The variable "${key}" is forgotten or empty.`);
  }
  return value;
}
