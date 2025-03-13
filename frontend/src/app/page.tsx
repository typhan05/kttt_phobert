import SearchForm from "@/components/SearchForm";

export const dynamic = "force-dynamic";

export default function Home() {
  return (
    <div className="min-w-screen min-h-screen bg-gray-800 flex items-center justify-center px-5 py-5">
      <SearchForm />
    </div>
  );
}
