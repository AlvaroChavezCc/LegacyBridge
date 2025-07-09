import { parsePaginationParams } from "./format_parameters.js";

const handlePaginationRequest = async ({
  req,
  res,
  next,
  getDataFn,
  extraParams = () => ({}),
}) => {
  try {
    const { page, limit, offset } = parsePaginationParams(req.query);
    const params = { limit, offset, ...extraParams(req.query) };

    const result = await getDataFn(params);
    const total = result.length > 0 ? Number(result[0].total) : 0;

    if (total === 0)
      return res.status(404).json({ message: "No hay datos para mostrar" });

    const totalPages = Math.ceil(total / limit);
    const data = result.map(({ total, ...rest }) => rest);

    res.status(200).json({
      data,
      total,
      count: data.length,
      limit,
      page,
      totalPages,
    });
  } catch (error) {
    next(error);
  }
};

export default handlePaginationRequest;
