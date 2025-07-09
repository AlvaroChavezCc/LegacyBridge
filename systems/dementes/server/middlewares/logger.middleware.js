export const requestLogger = (req, res, next) => {
  const { method, path, body, query } = req;

  console.log("📥 Incoming Request");
  console.log(`🟢 Method: ${method}`);
  console.log(`📍 Path:   ${path}`);
  console.log(`📦 Query:  ${JSON.stringify(query)}`);
  if (Object.keys(body || {}).length > 0) {
    console.log(`📝 Body:   ${JSON.stringify(body)}`);
  }
  console.log("—".repeat(40));

  next();
};
