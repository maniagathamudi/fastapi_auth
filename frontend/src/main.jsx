import { createRoot } from "react-dom/client";
import { Auth0Provider } from "@auth0/auth0-react";
import { BrowserRouter } from "react-router-dom";

import "./index.css";
import App from "./App.jsx";

createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Auth0Provider
      domain="dev-myzyu2t2reyac3bl.us.auth0.com"
      clientId="lXXb89Gf29hQSS4k1h6B0kD3bzpiVHeX"
      authorizationParams={{
        redirect_uri: window.location.origin
      }}
      cacheLocation="localstorage"
      useRefreshTokens={true}
    >
      <App />
    </Auth0Provider>
  </BrowserRouter>
);