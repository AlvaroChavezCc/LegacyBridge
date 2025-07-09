import app from "./server/app.js";
import { PORT } from "./server/config/env.js";

app.listen(PORT, () => {
  console.log(`🚀 Servidor escuchando en el puerto ${PORT}`);
});
