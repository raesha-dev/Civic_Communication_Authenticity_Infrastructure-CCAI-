"use client";

import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import en from "../../public/translations/en.json";
import es from "../../public/translations/es.json";
import fr from "../../public/translations/fr.json";
import hi from "../../public/translations/hi.json";

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: en },
      es: { translation: es },
      fr: { translation: fr },
      hi: { translation: hi },
    },
    lng: "en", // default
    fallbackLng: "en",
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
