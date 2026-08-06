import { useState, useEffect, useCallback } from "react";
import {
  getPredictionHistory,
  deletePrediction,
} from "../services/historyService";

export default function useHistory() {
  const [history, setHistory] = useState([]);

  const [page, setPage] = useState(1);

  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");

  const [prediction, setPrediction] = useState("");

  const [totalPages, setTotalPages] = useState(1);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // ======================================
  // Debounce Search (400ms)
  // ======================================
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search);
    }, 400);

    return () => clearTimeout(timer);
  }, [search]);

  // ======================================
  // Reset Page when Search/Filter Changes
  // ======================================
  useEffect(() => {
    setPage(1);
  }, [debouncedSearch, prediction]);

  // ======================================
  // Load History
  // ======================================
  const loadHistory = useCallback(async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getPredictionHistory({
        page,
        search: debouncedSearch,
        prediction,
      });

      console.log("History API Response:", data);

      const historyData =
        data.items || data.predictions || data.history || data.data || [];

      setHistory(Array.isArray(historyData) ? historyData : []);

      setTotalPages(data.totalPages || data.pages || data.total_pages || 1);
    } catch (err) {
      console.error(err);

      setHistory([]);

      setError(err.response?.data?.message || "Unable to load history.");
    } finally {
      setLoading(false);
    }
  }, [page, debouncedSearch, prediction]);

  // ======================================
  // Load Data
  // ======================================
  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  // ======================================
  // Delete Prediction
  // ======================================
  const removePrediction = async (id) => {
    try {
      await deletePrediction(id);

      setHistory((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      console.error(err);

      alert(err.response?.data?.message || "Failed to delete prediction.");
    }
  };

  return {
    history,

    page,
    setPage,

    search,
    setSearch,

    prediction,
    setPrediction,

    totalPages,

    loading,
    error,

    removePrediction,

    reloadHistory: loadHistory,
  };
}
