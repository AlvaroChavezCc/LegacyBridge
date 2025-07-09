export const unknownEndpoint = (req, res) => {
  console.error("❎ Estado: 404");
  console.error("📧 Mensaje: unkown endpoint");
  console.log("—".repeat(40));
  return res.status(404).send({ error: "unknown endpoint" });
};

export const errorHandler = (error, req, res, next) => {
  console.error("❎ Estado: 500");
  console.error("📧 Mensaje:", error.message);
  console.log("—".repeat(40));
  return res.status(500).json({ message: error.message });
};
